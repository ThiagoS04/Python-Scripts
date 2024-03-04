#Thiago Schuck September 13 2023
#This program calculates the average pH of a set of samples and classifies them as acidic, basic or neutral
def main():
    #Declare variables
    samples = 7.9, 8.3, 8, 8.3, 7.9, 7.8, 8.6
    averagePH = 0

    #Get average pH
    averagePH = ph_average(samples)

    #Display average pH
    print("The average pH is: ", averagePH)

    #Classify pH
    classify_ph(samples)

#Function to calculate average pH
def ph_average(samples):
    averagePH = 0
    for sample in samples:
        averagePH += sample
    averagePH /= len(samples)
    return averagePH

#Function to classify pH
def classify_ph(samples):
    i = 1
    for sample in samples:
        if sample < 7:
            print("Sample", i, "is acidic")
        elif sample > 7:
            print("Sample", i, "is basic")
        else:
            print("Sample", i, "is neutral")
        i += 1

if __name__ == "__main__":
    main()
    