import json
import time
import gc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


def get_opening_hours(driver, place_url):
    try:
        print(f"\nFetching URL: {place_url}")
        driver.get(place_url)
        
        wait = WebDriverWait(driver, 3)
        
        try:
            list_operation = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "list_operation")))
            
            more_button = driver.find_element(By.CSS_SELECTOR, ".btn_more")
            more_button.click()
            print("Clicked more button")
            
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".fold_floor")))
            
            opening_hours = []
            
            operation_items = driver.find_elements(By.CSS_SELECTOR, ".fold_floor .displayPeriodList:first-child .list_operation li")
            for item in operation_items:
                time_span = item.find_element(By.CSS_SELECTOR, ".time_operation")
                full_text = f"{item.text.replace(time_span.text, '')} {time_span.text}".strip()
                if full_text:
                    print(f"Found regular hours: {full_text}")
                    opening_hours.append(full_text)
            
            try:
                holiday_items = driver.find_elements(By.CSS_SELECTOR, ".fold_floor .displayPeriodList:nth-child(2) .list_operation li")
                for item in holiday_items:
                    time_span = item.find_element(By.CSS_SELECTOR, ".time_operation")
                    full_text = f"공휴일 {time_span.text}".strip()
                    if full_text:
                        print(f"Found holiday hours: {full_text}")
                        opening_hours.append(full_text)
            except:
                print("No holiday hours found")
            
            # TODO: 관련하여 발생하는 에러 처리
            try:
                close_button = driver.find_element(By.CSS_SELECTOR, ".fold_floor .btn_close")
                close_button.click()
                print("Closed hours viewer")
            except:
                print("Could not close hours viewer")
            
            print(f"Final opening hours: {opening_hours}")
            return opening_hours
            
        except TimeoutException:
            print("No opening hours found, skipping...")
            return []
            
    except Exception as e:
        print(f"Error fetching opening hours: {e}")
        return []


def get_images(driver, place_url):
    try:
        print("\nFetching images...")
        images = []
        seen_urls = set()
        
        try:
            frame = driver.find_element(By.CSS_SELECTOR, ".frame_g")
            frame.click()
            print("Clicked image viewer")
            
            wait = WebDriverWait(driver, 3)
            viewer = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".view_image")))
            print("Image viewer loaded")
            
            prev_url = None
            retry_count = 0
            
            while len(images) < 5 and retry_count < 10:
                try:
                    current_img = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".view_image img.img_photo")))
                    img_url = current_img.get_attribute("src")
                    
                    if img_url:
                        if img_url.startswith("//"):
                            img_url = "https:" + img_url
                        
                        if img_url == prev_url:
                            retry_count += 1
                            time.sleep(0.5)
                            continue
                            
                        if img_url in seen_urls:
                            print("Found duplicate image, stopping")
                            break
                            
                        seen_urls.add(img_url)
                        images.append(img_url)
                        print(f"Found image {len(images)}: {img_url}")
                    
                    next_button = driver.find_element(By.CSS_SELECTOR, ".link_next")
                    next_button.click()
                    time.sleep(1)
                    
                except Exception as e:
                    print(f"Finished collecting images: {len(images)}")
                    break
            
            try:
                close_button = driver.find_element(By.CSS_SELECTOR, ".btn_close")
                close_button.click()
            except:
                print("Could not close viewer, continuing anyway")
            
        except Exception as e:
            print(f"Error with image viewer: {e}")
        
        if not images:
            print("No images found, using default image")
            return ["https://balm-bucket.s3.ap-northeast-2.amazonaws.com/images/place/place_default.jpg"]
        
        print(f"Successfully found {len(images)} images")
        return images
        
    except Exception as e:
        print(f"Error in get_images: {e}")
        return ["https://balm-bucket.s3.ap-northeast-2.amazonaws.com/images/place/place_default.jpg"]


options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(options=options)

try:
    with open('./place.json', 'r', encoding='utf-8') as file:
        places = json.load(file)

    transformed_places = []
    for i, place in enumerate(places):
        print(f"\nProcessing place {i+1}/{len(places)}: {place['place_name']}")
        
        opening_hours = get_opening_hours(driver, place['place_url'])
        images = get_images(driver, place['place_url'])
        
        place['opening_hours'] = opening_hours
        place['image_urls'] = images
        
        transformed_places.append(place)
        time.sleep(1)
        
        if i % 10 == 0:
            gc.collect()

    with open('./place.json', 'w', encoding='utf-8') as file:
        json.dump(transformed_places, file, ensure_ascii=False, indent=2)
except Exception as e:
    print(f"Error processing places: {e}")
finally:
    driver.quit()