import pandas as pd

class MovieRecommender:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = self.load_dataset()

    def load_dataset(self):
        try:
            return pd.read_csv(self.file_path)
        except FileNotFoundError:
            print(f"Error: The file '{self.file_path}' was not found.")
            exit()

    def recommend_movies(self, genre, max_duration, min_year):
        condition = (
            (self.df['Genre'] == genre) & 
            (self.df['Duration_Minutes'] <= max_duration) & 
            (self.df['Release_Year'] >= min_year)
        )
        filtered_df = self.df[condition].copy()
        
        if not filtered_df.empty:
            filtered_df['Popularity_Score'] = filtered_df['User_Rating'] * (filtered_df['Vote_Count'] / 1000000)
            return filtered_df.sort_values(by='Popularity_Score', ascending=False)
        
        return filtered_df

def get_user_inputs(valid_genres):
    print("--- WELCOME TO YOUR MOVIE RECOMMENDATION ASSISTANT v2.0 ---\n")
    
    genre = input(f"What genre? ({', '.join(valid_genres)}): ").strip().title()
    if genre in ["Sci-Fi", "Scifi", "Sci-fi"]:
        genre = "Sci-Fi"
        
    while True:
        try:
            max_duration = int(input("Maximum duration (in minutes)?: "))
            if max_duration > 0:
                break
            print("Please enter a positive number.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            
    while True:
        try:
            min_year = int(input("Released after which year (e.g., 2000)?: "))
            if 1900 <= min_year <= 2026:
                break
            print("Please enter a valid year between 1900 and 2026.")
        except ValueError:
            print("Invalid input. Please enter a valid year.")
            
    return genre, max_duration, min_year

if __name__ == "__main__":
    recommender = MovieRecommender('movies_dataset.csv')
    unique_genres = recommender.df['Genre'].unique()
    
    requested_genre, max_duration, min_year = get_user_inputs(unique_genres)
    recommendations = recommender.recommend_movies(requested_genre, max_duration, min_year)
    
    print("\n--- OUR RECOMMENDATIONS (Sorted by Popularity Score) ---")
    if recommendations.empty:
        print(f"Sorry, no {requested_genre} movies found matching your criteria.")
    else:
        output_cols = ['Title', 'Genre', 'Duration_Minutes', 'User_Rating', 'Release_Year']
        print(recommendations[output_cols].to_string(index=False))