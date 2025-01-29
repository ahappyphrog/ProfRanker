import os
import sys
import asyncio
import ratemyprofessor
from bs4 import BeautifulSoup
from prettytable import PrettyTable
import math

print("Initiating RateMyProfessor")

school = ratemyprofessor.get_school_by_name("Cornell University")

async def process_professor(professor_name, instructor_names_lowered):
    professor_data = await asyncio.to_thread(ratemyprofessor.get_professors_by_school_and_name, school, professor_name)
    if professor_data:
        professor = professor_data[0]
        if professor.name.lower() in instructor_names_lowered:
            if professor.num_ratings != 0:
                print(f"Found profile for {professor.name.lower()}")
                return {
                    "name": professor.name.lower(),
                    "rating": professor.rating, 
                    "difficulty": professor.difficulty,
                    "ratings": professor.num_ratings,
                    "link": f"https://www.ratemyprofessors.com/professor/{professor.id}"
                }
            else: 
               print(f"Professor has no ratings. Filtering: {professor_name}") 
        else:
            print(f"Scraped professor name doesn't match original. Filtering: {professor_name} (Rate My Professor: {professor.name.lower()})")
            return None
    else:
        print(f"No Rate My Professor profile for: {professor_name}")
        return None

async def retrieve_data(instructor_names_lowered):
    tasks = [process_professor(name, instructor_names_lowered) for name in instructor_names_lowered]
    results = await asyncio.gather(*tasks)
    
    filtered_results = [result for result in results if result is not None]
    return filtered_results

def list_files_in_folder(folder):
    return [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f)) and not f.endswith('.py')]

def display_table(data):
    if data:
        table = PrettyTable(data[0].keys())
        for item in data:
            table.add_row(item.values())
        print(table)

def calculate_weighted_score(professor, w1, w2, w3):
    rating = professor["rating"]
    difficulty = professor["difficulty"]
    ratings = professor["ratings"]
    weighted_score = (rating * w1) + ((5 - difficulty) * w2) + (math.log(ratings + 1) * w3 *.8)
    return weighted_score

def remove_duplicates(professors):
    unique_professors = {}
    for professor in professors:
        unique_professors[professor["name"]] = professor
    return list(unique_professors.values())

def main():
    folder_path = os.path.dirname(os.path.realpath(__file__))
    files = list_files_in_folder(folder_path)

    if not files:
        print("No files found in the folder.")
        return

    print("Select a file to process:")
    for idx, file in enumerate(files):
        print(f"{idx + 1}. {file}")

    file_index = int(input("Enter the number of the file you want to select: ")) - 1
    selected_file = files[file_index]

    print("\nHow would you like to rank the instructors?")
    print("1. By Rating")
    print("2. By Difficulty")
    print("3. By Weighted Score")
    print("4. By All")

    rank_choice = int(input("Enter the number of your choice: "))
    
    if rank_choice == 1:
        rank_by = "rating"
    elif rank_choice == 2:
        rank_by = "difficulty"
    elif rank_choice == 3:
        rank_by = "weighted_score"
    elif rank_choice == 4:
        rank_by = "all"
    

    file_path = os.path.join(folder_path, selected_file)
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, 'html.parser')

    instructor_elements = soup.find_all('li', class_='instructors')

    instructor_set = set() 
    for element in instructor_elements:
        spans = element.find_all('span', class_='tooltip-iws')
        for span in spans:
            full_name = span.get('data-content').split('(')[0].strip() 
            instructor_set.add(full_name)

    instructor_names = sorted(list(instructor_set))
    instructor_names_lowered = [name.lower() for name in instructor_names]

    print(f"Total number of unique instructors scraped: {len(instructor_names_lowered)}")

    professor_list = asyncio.run(retrieve_data(instructor_names_lowered))

    professor_list = remove_duplicates(professor_list)

    if rank_by == "rating" or rank_by == "all":
        sorted_by_rating = sorted(professor_list, key=lambda x: x["rating"], reverse=True)
        print("\n\nProfessors ranked by rating:\n")
        display_table(sorted_by_rating)

    if rank_by == "difficulty" or rank_by == "all":
        sorted_by_difficulty = sorted(professor_list, key=lambda x: x["difficulty"])
        print("\n\nProfessors ranked by difficulty:\n")
        display_table(sorted_by_difficulty)

    if rank_by == "weighted_score" or rank_by == "all":
        print("\nEnter the weights for the algorithm (Enter for default 1):")
        w1 = input("Weight for Rating: ")
        w1 = float(w1) if w1.strip() else 1.0
        
        w2 = input("Weight for Difficulty: ")
        w2 = float(w2) if w2.strip() else 1.0
        
        w3 = input("Weight for Number of Ratings: ")
        w3 = float(w3) if w3.strip() else 1.0
        
        for professor in professor_list:
            professor["weighted_score"] = calculate_weighted_score(professor, w1, w2, w3)
        
        sorted_by_weighted_score = sorted(professor_list, key=lambda x: x["weighted_score"], reverse=True)
        print("\n\nProfessors ranked by weighted score:\n")
        display_table(sorted_by_weighted_score)

    print(f"{len(professor_list)} of {len(instructor_names_lowered)} professors retrieved from Rate My Professor")

main()
