from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_daraz_laptops():
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(options=chrome_options)
    
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    try:
        url = "https://www.daraz.com.np/catalog/?spm=a2a0e.tm80335409.search.d_go&q=laptop"
        driver.get(url)
        
        print("Loading page...")
        product_selectors = [
            "div[data-qa-locator='product-item']",
            ".gridItem",
            ".c2prKC",
            ".buTCk",
            ".RfADt",
            "[data-item-id]"
        ]
        
        products = []
        
        for selector in product_selectors:
            try:
                # Wait up to 15 seconds for products to appear
                WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                )
                
                # Get all product elements
                product_elements = driver.find_elements(By.CSS_SELECTOR, selector)
                print(f"✓ Found {len(product_elements)} products using selector: {selector}")
                
                if product_elements:
                    products = product_elements
                    break
                    
            except Exception as e:
                print(f"✗ Selector '{selector}' didn't work: {str(e)[:100]}")
                continue
        
        if not products:
            print("No products found with any selector. Let's inspect the page structure...")
            
            # Wait a bit more and get page source
            time.sleep(10)
            page_source = driver.page_source
            
            # Save for inspection
            with open('daraz_selenium_debug.html', 'w', encoding='utf-8') as f:
                f.write(page_source)

            # Parse
            soup = BeautifulSoup(page_source, 'html.parser')
            
            # Look for common product container patterns
            potential_products = soup.find_all('div', attrs={
                'data-qa-locator': True
            }) or soup.find_all('div', class_=lambda x: x and 'item' in str(x).lower())
            
            print(f"Found {len(potential_products)} potential product elements")
            
            if potential_products:
                print("Sample product attributes:")
                for i, product in enumerate(potential_products[:3]):
                    print(f"Product {i+1}:")
                    print(f"  Classes: {product.get('class')}")
                    print(f"  Attributes: {dict(product.attrs)}")
                    print("  " + "-"*50)
            
            return []
        
        # Extract product information
        product_data = []
        
        for i, product in enumerate(products[:20]):  # Limit to first 20 products
            try:
                # Get product HTML for detailed parsing
                product_html = product.get_attribute('outerHTML')
                product_soup = BeautifulSoup(product_html, 'html.parser')
                
                # Extract product details
                title_elem = (
                    product_soup.find('img', {'alt': True}) or
                    product_soup.find('a', {'title': True}) or
                    product_soup.find('h3') or
                    product_soup.find('div', class_=lambda x: x and 'title' in str(x).lower())
                )
                
                price_elem = (
                    product_soup.find('span', class_=lambda x: x and 'price' in str(x).lower()) or
                    product_soup.find('div', class_=lambda x: x and 'price' in str(x).lower()) or
                    product_soup.find(string=lambda text: text and 'Rs' in text)
                )
                
                link_elem = product_soup.find('a', href=True)
                
                # Extract data
                title = ""
                if title_elem:
                    title = title_elem.get('alt') or title_elem.get('title') or title_elem.get_text(strip=True)
                
                price = ""
                if price_elem:
                    if hasattr(price_elem, 'get_text'):
                        price = price_elem.get_text(strip=True)
                    else:
                        price = str(price_elem).strip()
                
                link = ""
                if link_elem:
                    link = link_elem.get('href')
                    if link and not link.startswith('http'):
                        link = "https://www.daraz.com.np" + link
                
                if title or price:  # Only add if we found some data
                    product_data.append({
                        'title': title,
                        'price': price,
                        'link': link
                    })
                    print(f"Product {i+1}: {title[:50]}... - {price}")
                
            except Exception as e:
                print(f"Error processing product {i+1}: {e}")
                continue
        
        return product_data
        
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
        
    finally:
        driver.quit()

def main():
    print("Starting Daraz laptop scraping...")
    products = scrape_daraz_laptops()
    
    if products:
        # Create DataFrame and save to CSV
        df = pd.DataFrame(products)
        df.to_csv('daraz_laptops.csv', index=False, encoding='utf-8')
        df.to_json('daraz_laptops.json', orient='records', indent=2)
        print(f"\n✓ Successfully scraped {len(products)} products!")
        print("Data saved to 'daraz_laptops.csv' and 'daraz_laptops.json'")
        print("\nFirst 5 products:")
        print(df.head())
    else:
        print("No products were scraped. Check the debug files for more information.")

if __name__ == "__main__":
    main()