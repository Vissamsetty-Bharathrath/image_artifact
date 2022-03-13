import numpy as np
import cv2
#import matplotlib.pyplot as plt
#import matplotlib.image as mpimg

BLOCK_ROWS = 5
BLOCK_COLS = 5
KERNEL_X = 3
KERNEL_Y = 3

T_FLAT = True
T_TEX =  False

class ArtifactedBlock :

# constructor used to assign values

    def __init__ (self , x_coord , y_coord , annoyance ):
        self .x = x_coord
        self .y = y_coord
        self .annoyance = annoyance

#used for highlighting artifacts on image 

def highlight_image_artifacts (image , artifacted_blocks ):
    for block in artifacted_blocks :
        start_point = block .y* BLOCK_COLS , block .x* BLOCK_ROWS
        end_point = (block .y+1)* BLOCK_COLS ,(block .x+1)* BLOCK_ROWS
        cv2. rectangle (image , start_point,end_point , (0 ,0 ,0))

#calculating the total visibility

def compute_overall_annoyance ( artifacted_blocks ):
    annoyance = 0
    if len( artifacted_blocks ) != 0:
        for block in artifacted_blocks :
            annoyance = annoyance + block.annoyance
        return annoyance  / len( artifacted_blocks )
    else :
        return 0

#conditions to satisfy whether block is artifacted

def check_if_artifacted ( blocks_SADs ):
    F = blocks_SADs < T_FLAT
    T = blocks_SADs > T_TEX
    #print(F[0][0])
    flat_top = (all(F [0][0]) and all(F [0][1])) or (all(F [0][1]) and all(F[0][2]))
    flat_bottom = (all(F [2][0]) and  all(F [2][1])) or (all(F [2][1]) and all(F[2][2]))
    flat_left = (all(F [0][0]) and all(F [1][0])) or (all(F [1][0]) and  all(F[2][0]))
    flat_right = (all(F [0][2]) and all(F [1][2])) or ( all(F [1][2]) and  all(F[2][2]))
    flat = flat_top or flat_bottom or flat_left or flat_right
    tex = False
    for i in range (0, len (T)):
        for j in range (0, len (T[i])):
            if i != 1 and j != 1:
                tex = tex or all(T[i][j])
    centre = ( T_FLAT < all (blocks_SADs [1][1])) and (all (blocks_SADs [1][1]) < T_TEX )
    artifacted = tex and flat and centre
    return artifacted

#checking for the artifacted blocks
def check_artifacted_blocks ( blocks_SADs_map ):
    artifacted_blocks = []
    for i in range (1, len ( blocks_SADs_map ) - 1):
        for j in range (1, len ( blocks_SADs_map [i]) - 1):
            if check_if_artifacted ( blocks_SADs_map [i -1:i+2, j -1:j +2]) :
                annoyance = blocks_SADs_map [i][j ]/(( BLOCK_COLS -1) *(BLOCK_ROWS -1) *2)
                artifacted_blocks.append ( ArtifactedBlock (i,j, annoyance ))
    return artifacted_blocks

#Sum of Absolute Differences and Detection Kernel-1 for single block  
def compute_SAD_for_block ( block ):
    sad = 0
    for i in range (0, BLOCK_ROWS-1) :
        for j in range (0, BLOCK_COLS-1) :
            sad = sad + np.abs ( block [i][j] - block [i +1][ j])+ np.abs ( block [i][j]- block [i][j +1])
    return sad

#Sum of Absolute Differences and Detection Kernel-2 for blocks   
def compute_blocks_SAD ( blocks ):
    blocks_SADs = np. array ([[[0 ,0 ,0] for x in range (len( blocks [0]) )] for x in range ( len( blocks ))])
    for i in range (0, len ( blocks )):
        for j in range (0, len ( blocks [i])):
            blocks_SADs [i][j] = compute_SAD_for_block ( blocks [i][j])
    return blocks_SADs

#Sum of Absolute Differences and Detection Kernel-2  

#getting the block from image

def get_image_blocks (image , rows , cols ):
    blocks = []

    for i in range (0, int (rows / BLOCK_ROWS) ):
        blocks . append ([])
        for j in range (0, int(cols / BLOCK_COLS) ):
            blocks [i]. append ( image [i* BLOCK_ROWS :(i +1)* BLOCK_ROWS
            , j*BLOCK_COLS :(j+1)* BLOCK_COLS ])

    return blocks

#main function to call all functions

def measure_artifacts (image_path,output_path):
    image = cv2. imread (image_path)
    image_array = np. array (image , dtype =np. int64 )
    print (" reading image "+ image_path)
    rows , cols , ch = image . shape
    blocks = get_image_blocks ( image_array , rows , cols )
    blocks_SADs = compute_blocks_SAD ( blocks )
    print(len(blocks_SADs))
    artifacted_blocks = check_artifacted_blocks ( blocks_SADs )
    annoyance_score = np. average ( compute_overall_annoyance ( artifacted_blocks))
    print ('Annoyance Score:',float("{:.2f}".format(annoyance_score)))
    total_artifacts_percentage = np. float_ ( len( artifacted_blocks )) / np.float_ (( rows / BLOCK_ROWS )
    *( cols / BLOCK_COLS )) * 100
    print ('Artifacted Edges:' ,float("{:.2f}".format(total_artifacts_percentage)))
    highlight_image_artifacts (image , artifacted_blocks )
    cv2 . imwrite ( output_path, image)
    return ( total_artifacts_percentage , annoyance_score )
image_output = measure_artifacts(r"C:\Users\Vissamsetty Bharath\Documents\project_python\image-022.jpg"
,r"C:\Users\Vissamsetty Bharath\Documents\project_python\test_write.jpg")
#print(image_output)


"""
def image_out(original,modified):
    plt.subplot(1,2,1)
    plt.imshow(original)
    plt.subplot(1,2,2)
    plt.imshow(modified)
    plt.show()

"""