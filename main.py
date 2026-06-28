import pandas as pd
import os

class MovieRecommender:
    def __init__(self, dataset_path):
        self.dataset_path = dataset_path
        self.movies_df = None
        self.genre_col = 'genre'
        self.load_dataset()

    def load_dataset(self):
        if not os.path.exists(self.dataset_path):
            data = {
                'title': ['Inception', 'Interstellar', 'The Dark Knight', 'The Notebook', 'La La Land'],
                'genre': ['Action|Sci-Fi', 'Sci-Fi|Drama', 'Action|Drama', 'Romance|Drama', 'Romance|Musical'],
                'duration': [148, 169, 152, 123, 128]
            }
            self.movies_df = pd.DataFrame(data)
            self.movies_df.to_csv(self.dataset_path, index=False)
        else:
            self.movies_df = pd.read_csv(self.dataset_path, quotechar='"', skipinitialspace=True)
        
        for col in self.movies_df.columns:
            if col.lower().strip() in ['genre', 'genres']:
                self.genre_col = col
                break
                
        self.movies_df[self.genre_col] = self.movies_df[self.genre_col].fillna('').str.lower()

    def get_sample_genres(self):
        if self.movies_df is not None and not self.movies_df.empty:
            all_genres = self.movies_df[self.genre_col].dropna().unique()
            clean_genres = set()
            for g in all_genres:
                for sub_g in str(g).replace('|', ',').replace('/', ',').split(','):
                    sub_g = sub_g.strip().title()
                    if sub_g:
                        clean_genres.add(sub_g)
            sample = list(clean_genres)[:4]
            return ", ".join(sample)
        return "Sci-Fi, Action"

    def get_recommendations(self, target_genre, max_duration):
        if self.movies_df is None or self.movies_df.empty:
            return pd.DataFrame()

        target_genre = target_genre.lower().strip()
        
        dur_col = 'duration'
        for col in self.movies_df.columns:
            if col.lower().strip() in ['duration', 'runtime', 'duration_minutes', 'durée']:
                dur_col = col
                break

        if dur_col not in self.movies_df.columns:
            print(f"❌ Critical Error: Column '{dur_col}' not found.")
            return pd.DataFrame()

        mask = (self.movies_df[dur_col] <= max_duration) & (self.movies_df[self.genre_col].str.contains(target_genre, case=False, na=False, regex=False))
        filtered_df = self.movies_df[mask]
        
        return filtered_df.sort_values(by=dur_col, ascending=True)

if __name__ == "__main__":
    print("🎬 === WELCOME TO YOUR CINEMA ASSISTANT V2 (FINAL) ===")
    
    recommender = MovieRecommender(dataset_path="movies_dataset.csv")
    
    sample_genres = recommender.get_sample_genres()
    
    user_genre = input(f"\n👉 Enter a movie genre (e.g., {sample_genres}...): ")
    user_duration_input = input("👉 Enter your maximum available time (in minutes): ")
    
    try:
        user_duration = int(user_duration_input)
    except ValueError:
        user_duration = 120

    results = recommender.get_recommendations(user_genre, user_duration)
    
    print("\n📊 === SEARCH RESULTS ===")
    if results.empty:
        print(f"😢 Sorry, no '{user_genre}' movies match your criteria.")
    else:
        print(f"🎉 Here are the best movies found ({len(results)} matches):\n")
        
        title_col = 'title'
        for col in results.columns:
            if col.lower().strip() in ['title', 'titre', 'name']:
                title_col = col
                break
                
        dur_col = 'duration'
        for col in results.columns:
            if col.lower().strip() in ['duration', 'runtime', 'duration_minutes', 'durée']:
                dur_col = col
                break
                
        for index, row in results.iterrows():
            print(f"🎥 {str(row[title_col]).title()} | Genre: {str(row[recommender.genre_col]).upper()} | Duration: {row[dur_col]} min")
            
    print("\n=======================================================")
