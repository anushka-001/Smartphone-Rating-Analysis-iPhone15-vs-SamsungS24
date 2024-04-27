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
        
        # Check if the request was successful
        if response.status_code != 200:
            print(f"Failed to fetch page {page} with status code {response.status_code}.")
            break

        soup = BeautifulSoup(response.text, 'html.parser')
        reviews = soup.findAll('div', {'data-hook': 'review'})

        if not reviews:
            print(f"No reviews found on page {page}. Possible end of reviews or error.")
            # Optionally, check for a known element that appears when no more reviews are available
            no_reviews_message = soup.find('div', text=lambda t: t and "no reviews match" in t.lower())
            if no_reviews_message:
                print("No more reviews available according to the page.")
                break
            continue  # If unsure, try next page
        
        for item in reviews:
            if collected_reviews >= max_reviews:
                print("Reached the maximum number of reviews specified.")
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
    
    # Splitting the reviews into two parts
    half = len(reviews) // 2
    reviews_part1 = reviews[:half]
    reviews_part2 = reviews[half:]

    df_part1 = pd.DataFrame(reviews_part1)
    df_part2 = pd.DataFrame(reviews_part2)

    df_part1.to_excel("output_part1.xlsx", index=False)
    df_part2.to_excel("output_part2.xlsx", index=False)

if __name__ == "__main__":
    main()
