import pandas as pd

# Create a DataFrame with first, middle, and last names
data = {
    "First Name": [
        "Barack", "Elon", "Oprah", "Leonardo", "Angelina",
        "Jennifer", "Robert", "Scarlett", "Kanye"
    ],
    "Middle Name": [
        "Hussein", "", "", "", "Jolie",
        "", "", "", ""
    ],
    "Last Name": [
        "Obama", "Musk", "Winfrey", "DiCaprio", "Jolie",
        "Aniston", "Downey", "Johansson", "West"
    ]
}

# Ensure all middle names are empty strings if not provided
data["Middle Name"] = [middle.strip() if middle else "" for middle in data["Middle Name"]]

# Convert the dictionary to a DataFrame
df = pd.DataFrame(data)

# Save the DataFrame to an Excel file
df.to_excel("famous_people.xlsx", index=False)
print("Excel file created successfully!")
