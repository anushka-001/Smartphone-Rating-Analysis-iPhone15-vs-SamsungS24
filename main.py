import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def extract_reviews(review_url, max_reviews):
    review_list = []
    page = 1
    collected_reviews = 0

    while collected_reviews < max_reviews:
        formatted_url = review_url.format(page=page)
        response = requests.get(formatted_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        reviews = soup.findAll('div', {'data-hook': 'review'})

        if not reviews:
            print("No more reviews found.")
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
        time.sleep(1)  # Pause for a second to avoid rapid requests

    return review_list

def main():
    product_url = "https://www.amazon.in/Apple-iPhone-15-128-GB/dp/B0CHX3TW6X"
    review_url = product_url.replace("dp", "product-reviews") + "?pageNumber={page}"
    max_reviews = 264  # Total number of reviews you want to collect
    reviews = extract_reviews(review_url, max_reviews)
    
    df = pd.DataFrame(reviews)
    df.to_excel("output.xlsx", index=False)

if __name__ == "__main__":
    main()
