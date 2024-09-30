# Script that will go through and count all of the frames and then print out total time for each object. 
import argparse
import pandas as pd
import os

# Initialize the argument parser and add fields for the arguments
parser = argparse.ArgumentParser(description="Read a passed CSV file")
parser.add_argument('csv_file', type=str, help='path to csv file')
parser.add_argument('output_directory', type=str, help='path for the output file')

# Gather the arguments
args = parser.parse_args()

# Read through the csv file and gather information for each frame
try:
    df = pd.read_csv(args.csv_file, header=1)

    if df.shape[1] < 2:
        print('CSV file has less than two columns, inadequate file')
    else:
        # Create the output directory
        os.makedirs(args.output_directory, exist_ok=True)
        # Create the text file
        output_file = os.path.join(args.output_directory, 'frames_quantified.txt')

        # Extract first and second column from the csv
        first_column = df.iloc[:,0]
        second_column = df.iloc[:,1]

        # Write the values to the text file
        with open(output_file, 'w') as f:
            timeDictionary = {"left": 0, "right": 0, "no": 0} 
            frameDictionary = {"left": [], "right": [], "no": []}
            current_val = second_column.iloc[0]
            current_start_frame = first_column.iloc[0]
            
            for first_val, second_val in zip(first_column, second_column):
                # Count up total frames that mouse was focused on object
                timeDictionary[second_val] += 1
                
                # Count up the time that the mouse spent on each object for each interaction
                if second_val != current_val:
                    frameDictionary[current_val].append([current_start_frame, first_val - 1])
                    current_val = second_val
                    current_start_frame = first_val
            # Append the last interaction after the loop ends
            frameDictionary[current_val].append([current_start_frame, first_column.iloc[-1]])

            # Now write out to the output file
            for key in timeDictionary:
                # Write total time spent for each object
                f.write(f'Total time spent on {key}: {timeDictionary[key] / 30:0.2f} seconds\n')

            for key in frameDictionary:
                # Write time spent during each interaction of the object
                f.write(f'Time spent for each {key} interaction:\n')
                for val in timeDictionary[key]:
                    interaction_time = (val[1] - val[0]) / 30
                    f.write(f'  Interaction from frame {val[0]} to {val[1]}: {interaction_time:0.2f} seconds\n')
        print(f"First and second column values successfully saved to {output_file}")

except FileNotFoundError:
    print("File couldn't be found")
except Exception as e:
    print(f"Error: {e}")