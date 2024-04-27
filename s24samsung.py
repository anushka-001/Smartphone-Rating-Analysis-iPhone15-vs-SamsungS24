import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def extract_reviews(review_url, max_reviews):
    review_list = []
    page = 1
    collected_reviews = 0

    while collected_reviews < max_reviews:
        formatted_url = review_url + "&pageNumber=" + str(page)
        print("Fetching reviews from:", formatted_url)  # Debugging output
        response = requests.get(formatted_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        reviews = soup.findAll('div', {'data-hook': 'review'})

        # Debugging: check if reviews are found
        if not reviews:
            print(f"No reviews found on page {page}. Checking if no more pages are available...")
            no_more_reviews = soup.find('div', text='Sorry, no reviews match your current selections.')  # Update with actual text if different
            if no_more_reviews:
                print("No more reviews available according to the page message.")
                break
            else:
                print("No reviews elements found but no end message. Possible end of reviews or error.")
                break
        
        for item in reviews:
            if collected_reviews >= max_reviews:
                break
            review = {
                'Product Title': soup.title.text.replace("Amazon.in:Customer reviews: ", ""),
                'Review Title': item.find('a', {'data-hook': 'review-title'}).text.strip(),
                'Rating': item.find('i', {'data-hook': 'review-star-rating'}).text.strip(),
                'Review Body': item.find('span', {'data-hook': 'review-body'}).text.strip(),
                'Review Date': item.find('span', {'data-hook': 'review-date'}).text.strip(),
            }
            review_list.append(review)
            collected_reviews += 1
        
        page += 1  # Increment page count for pagination
        time.sleep(2)  # Increase delay to be more conservative with requests

    return review_list

def main():
    review_url = "https://www.amazon.in/product-reviews/B0CS5VFZMT/ref=cm_cr_dp_mb_top?"
    max_reviews = 100  # Adjust based on how many reviews you actually need
    reviews = extract_reviews(review_url, max_reviews)
    
    df = pd.DataFrame(reviews)
    df.to_excel("output.xlsx", index=False)

if __name__ == "__main__":
    main()
