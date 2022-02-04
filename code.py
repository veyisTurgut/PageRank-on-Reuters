## ADALET VEYİS TURGUT
import sys
def computeAdjacenyMatrix(filename):
    webpages = []
    with open(filename, "r") as f:
        first_line = f.readline()
        number_of_vertices = int(first_line[first_line.index(' '):])
        for _ in range(number_of_vertices):
            webpages.append(f.readline().split(' ')[1][1:-2])
        adjacency_matrix = [[ 0 for _ in range(number_of_vertices) ] for _ in range(number_of_vertices)]
        f.readline() # *Edges
        for line in f:
            edge1, edge2 = line.split()
            adjacency_matrix[int(edge1)-1][int(edge2)-1] = 1
    return webpages, adjacency_matrix

def makeGraphUndirected(adjacency_matrix):
    # For each edge vertex1 vertex2, include an edge in the opposite direction
    for i in range(len(adjacency_matrix)):
        for j in range(len(adjacency_matrix)):
            if adjacency_matrix[i][j] == 1:
                adjacency_matrix[j][i] = 1
    return adjacency_matrix

def computeProbabilityMatrix(adjacency_matrix, transportation_rate):
    for i,row in enumerate(adjacency_matrix):
        if row.count(1) == 0: # If a raw in A has no 1, then replace each element by 1/N;
            adjacency_matrix[i] = [x / len(row) for x in row]
        else: 
            # Divide each 1 in a row by the numbers of 1s in that row
            # Multiply the resulting matrix by 1-t ; (t is the teleportation rate)
            # Add t/N to every element of the matrix to obtain P
            adjacency_matrix[i] = [x / row.count(1) * (1-transportation_rate) + transportation_rate/len(row) for x in row]
    return adjacency_matrix

def calculatePowerMethod(vector, matrix):
    result = [] # final result
    for i in range(len(vector)):
        prod = 0
        for j in range(len(matrix[i])):
            prod += vector[j] * matrix[j][i]
        result.append(prod)
    return result

def sortWebpages(webpages, result_vector):
    result = []
    for i in range(len(webpages)):
        result.append([webpages[i], result_vector[i]])
    result.sort(reverse=True, key=lambda x: x[1]) # Sort by the score in descending order
    return result[:50]

def writeResultToFile(result, filename):
    with open(filename, "w") as f:
        for page in result:
            f.write("{:>15} {:.7f}\n".format(page[0],page[1]))

if __name__ == "__main__":
    input_filename = sys.argv[1]
    output_filename = "top50.txt"
    transportation_rate = 0.15
    webpages, adjacency_matrix = computeAdjacenyMatrix(input_filename)
    adjacency_matrix = makeGraphUndirected(adjacency_matrix)
    probability_matrix = computeProbabilityMatrix(adjacency_matrix,transportation_rate)
    x_vector  = [1/(len(probability_matrix)) for _ in probability_matrix]
    prev_power = calculatePowerMethod(x_vector, probability_matrix)
    
    i = 1
    while True:
        i += 1
        next_power = calculatePowerMethod(prev_power, probability_matrix)
        if sum([abs(x - y) for x,y in zip(prev_power,next_power)]) < 1e-10:
            break
        prev_power = next_power
    
    top_webpages = sortWebpages(webpages, next_power)
    writeResultToFile(top_webpages, output_filename)
    print("Done!\nTotal iteration count: {}\nResult is stored in '{}' file.".format(i,output_filename))
