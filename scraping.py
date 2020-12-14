# 10.3.3  1. Import Splinter and Beautiful Soup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt



# --------------------------------------------------------------------------
#### 10.5.3 Integrate MongoDB into this Scraping App 
# Intialize browser, create data dictionary, end the WebDriver and return scraped data
# --------------------------------------------------------------------------

def scrape_all():
   # 2. Initiate headless driver for deployment.  Set up Splinter
    executable_path = {'executable_path': 'chromedriver.exe'}    # ??Line not included in 10.5.3 code
    browser = Browser("chrome", executable_path="chromedriver", headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dictionary
    data = {
      "news_title": news_title,
      "news_paragraph": news_paragraph,
      "featured_image": featured_image(browser),
      "facts": mars_facts(),
      "last_modified": dt.datetime.now(),
      "hemisphere_info": hemisphere_info(browser)
    }

    # Stop webdriver and return data
    browser.quit()
    return data


# --------------------------------------------------------------------------
#### 10.3.3 Scrape News Title and Teaser 
# --------------------------------------------------------------------------

# 10.5.2 Add function News and Title Scrape -- around inside code; 
# Add "browser" to function telling Python to use this variable, define outside of the funtion. 

def mars_news(browser):                                

    # Inside loop is 10.3.3 (except try/except clause)
    # 3. Visit the mars nasa news site 
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    
    # a. Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # 4. Parse the HTML
    html = browser.html   
    news_soup = soup(html, 'html.parser')
    
    
    # Add try/except for error handling 10.5.2
    try:
        slide_elem = news_soup.select_one('ul.item_list li.slide') 

        # Use the parent element to find the first `a` tag and save it as `news_title` 
        news_title = slide_elem.find("div", class_='content_title').get_text()
    
        # Use the parent element to find the paragraph text 
        news_paragraph = slide_elem.find('div', class_="article_teaser_body").get_text()

    except AttributeError:
        return None, None


    return news_title, news_paragraph



# --------------------------------------------------------------------------
#### 10.3.4 Scrape Featured Images
# --------------------------------------------------------------------------

# 10.5.2 Add function around Image Scrape inside; 
# Add "browser" to function telling Python to use this variable, define outside of the funtion. 


def featured_image(browser):
    # Visit URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)


    # Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()


    # Find the more info button and click that
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.links.find_by_partial_text('more info')
    more_info_elem.click()


    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')


    # Add try/except for error handling 10.5.2
    try:
        # Find the relative image url 10.3.4
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")

    except AttributeError:
        return None

    # Use the base URL to create an absolute URL (f-string)
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
    
    return img_url



# --------------------------------------------------------------------------
#### 10.3.5 Scrape Mars Data: Mars Facts (witinin a table)
# --------------------------------------------------------------------------
# 10.5.2 Add function around Image Scrape inside; 
def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('http://space-facts.com/mars/')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html()




# --------------------------------------------------------------------------
#### Scrape Mars Hemisphere Images and URLS
#    Challenge Deliverable 2
# --------------------------------------------------------------------------
def hemisphere_info(browser):
    
    # 1. Use browser to visit the URL 
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    # # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # # 3. Write code to retrieve the image urls and titles for each hemisphere.

    # Verify Tag and Class of Thumbnail
    browser.is_element_present_by_css('a.product-item h3', wait_time=1) 

    image_products = browser.find_by_css('a.product-item h3')
    image_number=len(image_products)


    for i in range(0, image_number): 
       # List to hold img_url and title
        hemisphere = {}
        # Go to second page - each of the hemispheres
        thumb_click = browser.find_by_css('a.product-item h3')[i].click()
        # Get title information
        browser.is_element_present_by_css('div.content h2.title', wait_time=1) 
        hemisphere['title'] = browser.find_by_css('div.content h2.title').text
        # Get link to full resolution image
        browser.is_element_present_by_css('div.downloads li a', wait_time=1) 
        sample_find = browser.find_by_css('div.downloads li a')
        hemisphere['img_url'] = sample_find['href']
        hemisphere_image_urls.append(hemisphere)
        
        browser.back()


    # 4. Print the list that holds the dictionary of each image url and title.
    # hemisphere_image_urls

    # 5. Quit the browser
    browser.quit()
    return hemisphere_image_urls


# --------------------------------------------------------------------------
# 10.5.3 This last block of code tells Flask that our script is complete and ready for action. 
# The print statement will print out the results of our scraping to our terminal after 
# executing the code.
# --------------------------------------------------------------------------
if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())



