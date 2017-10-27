import numpy as np
import random

def sigmoid(z):
    return 1/(1+np.exp(-z))

def sigmoid_prime(z):
    return sigmoid(z)*(1-sigmoid(z))

###
### FOUR EQUATIONS OF BACKPROP
###

def compute_error_final(a_final, z_final, gold_label):
    '''
    computing this as if we were using a quadratic cost function like MSE
    '''
    error_final = (a_final - gold_label) * sigmoid_prime(z_final)
    return error_final
    
def compute_error_l(weights_lplus1, error_lplus1, z_l):
    '''
    move error backward from previous layer through weights and
    then through the activation function
    '''
    error_l = np.dot(weights_lplus1, error_lplus1) * sigmoid_prime(z_l)
    return error_l

def compute_dC_db_l(error_l):
    '''
    The gradient of the cost function WRT the biases of a layer (l)
    '''
    return error_l

def compute_dC_dW_l(error_l, activation_lminus1):
    '''
    The gradient of the cost function WRT the weights of a layer (l)
    '''
    return np.dot(error_l, activation_lminus1.T)


###
### GRADIENT DESCENT
###

def update_weights_l(weights_l, activation_lminus1, error_l, learning_rate):
    dC_dW = compute_dC_dW_l(error_l, activation_lminus1)
    new_weights= weights_l - (learning_rate*dC_dW).T
    return new_weights
 
def update_biases_l(biases_l, error_l, learning_rate):
    dC_db = compute_dC_db_l(error_l)
    new_biases = biases_l - learning_rate*dC_db
    return new_biases

def with_hidden_initialize_weights_biases(numFeatures, numHidden, numLabels):
    # Values are randomly sampled from a Gaussian with a standard deviation of:
    #     sqrt(6 / (numInputNodes + numOutputNodes + 1))
    W_1 = np.random.normal(size=(numFeatures,numHidden),
                           loc=0,
                           scale=(np.sqrt(6/numFeatures+numHidden+1)))
    b_1 = np.random.normal(size=(numHidden,1),
                           loc=0,
                           scale=(np.sqrt(6/numFeatures+numHidden+1)))
    W_2 = np.random.normal(size=(numHidden,numLabels),
                           loc=0,
                           scale=(np.sqrt(6/numHidden+numLabels+1)))
    b_2 = np.random.normal(size=(numLabels,1),
                           loc=0,
                           scale=(np.sqrt(6/numHidden+numLabels+1)))
    return W_1, b_1, W_2, b_2


def initialize_weights_biases(numFeatures, numLabels):
    # Values are randomly sampled from a Gaussian with a standard deviation of:
    #     sqrt(6 / (numInputNodes + numOutputNodes + 1))
    W_1 = np.random.normal(size=(numFeatures,numLabels),
                           loc=0,
                           scale=(np.sqrt(6/numFeatures+numLabels+1)))
    b_1 = np.random.normal(size=(numLabels,1),
                           loc=0,
                           scale=(np.sqrt(6/numFeatures+numLabels+1)))
    return W_1, b_1


def initialize_weights_biases_hidden(numFeatures, numHidden, numLabels):
    # Values are randomly sampled from a Gaussian with a standard deviation of:
    #     sqrt(6 / (numInputNodes + numOutputNodes + 1))
    W_1 = np.random.normal(size=(numFeatures,numHidden),
                           loc=0,
                           scale=(np.sqrt(6/numFeatures+numHidden+1)))
    b_1 = np.random.normal(size=(numHidden,1),
                           loc=0,
                           scale=(np.sqrt(6/numFeatures+numHidden+1)))
    W_2 = np.random.normal(size=(numHidden,numLabels),
                           loc=0,
                           scale=(np.sqrt(6/numHidden+numLabels+1)))
    b_2 = np.random.normal(size=(numLabels,1),
                           loc=0,
                           scale=(np.sqrt(6/numHidden+numLabels+1)))
    return W_1, b_1, W_2, b_2


def feedforward(X,W_1,b_1):
    ### LAYER 1
    z_1 = np.add( np.dot( W_1.T,X ), b_1 )
    a_1 = sigmoid(z_1)
    return z_1,a_1


def feedforward_hidden(X, W_1,b_1, W_2,b_2):
    ### LAYER 1
    z_1 = np.add( np.dot( W_1.T,X ), b_1 )
    a_1 = sigmoid(z_1)
    ### LAYER 2
    z_2 = np.add( np.dot( W_2.T,a_1 ), b_2 )
    a_2 = sigmoid(z_2)
    return z_1,a_1,z_2,a_2


def create_data():
    Xs=[]
    Ys=[]
    for i in range(10):
        for j in range(10):
            for k in range(10):
                num=str(i)+str(j)+str(k)
                if int(num) < 333:
                    label=np.array([1.,0.,0.])
                elif int(num) < 666:
                    label=np.array([0.,1.,0.])
                else:
                    label=np.array([0.,0.,1.])
                    
                X = np.ndarray(buffer=np.array([float(i),float(j),float(k)]),
                               shape=(3,1),
                               dtype=float)
                    
                Y = np.ndarray(buffer=label,
                               shape=(3,1),
                               dtype=float)
                    
                Xs.append(X)
                Ys.append(Y)
    return(Xs, Ys)

                
def no_hidden_layer_demo():

    Xs, Ys = create_data()
    
    learning_rate=.001

    example=0
    num_examples=100000

    W_1,b_1 = initialize_weights_biases(numFeatures=3,
                                        numLabels=3)
    
    while example<num_examples:
        
        i=random.randint(0,999)

        X=Xs[i]
        Y=Ys[i]
        
        z_1,a_1 = feedforward(X, W_1, b_1)
        
        error_final = compute_error_final(a_final=a_1, z_final=z_1, gold_label=Y)
        
        W_1 = update_weights_l(weights_l = W_1, 
                               activation_lminus1 = X, 
                               error_l = error_final, 
                               learning_rate = learning_rate)
        
        b_1 = update_biases_l(biases_l = b_1,
                              error_l = error_final,
                              learning_rate = learning_rate)

                    
        
        example+=1
        
        print(b_1)



                
def with_hidden_layer_demo():

    Xs, Ys = create_data()
    
    learning_rate=.001

    example=0
    num_examples=10000000

    W_1,b_1,W_2,b_2 = with_hidden_initialize_weights_biases(numFeatures=3,
                                                            numHidden=3,
                                                            numLabels=3)
    
    while example<num_examples:
        
        i=random.randint(0,999)

        X=Xs[i]
        Y=Ys[i]

                    
        z_1,a_1,z_2,a_2 = feedforward_hidden(X, W_1, b_1, W_2, b_2)
        
        error_final = compute_error_final(a_final=a_2, z_final=z_2, gold_label=Y)
        
        W_2 = update_weights_l(weights_l = W_2, 
                               activation_lminus1 = a_1, 
                               error_l = error_final, 
                               learning_rate = learning_rate)
        
        b_2 = update_biases_l(biases_l = b_2,
                              error_l = error_final,
                              learning_rate = learning_rate)
        
        
        error_l = compute_error_l(weights_lplus1 = W_2, 
                                  error_lplus1 = error_final, 
                                  z_l = z_1)
        
        W_1 = update_weights_l(weights_l = W_1, 
                               activation_lminus1 = X, 
                               error_l = error_l, 
                               learning_rate = learning_rate)
        
        b_1= update_biases_l(biases_l = b_1,
                             error_l = error_l,
                             learning_rate = learning_rate)
        
        
        example+=1

    ### VISUALIZATIONS !!! ###
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D

    # plotting
    
    data_plot={}
    for i in range(10):
        for j in range(10):
            for k in range(10):
                num=str(i)+str(j)+str(k)
                X=Xs[int(num)]
                
                if int(num) < 333:
                    
                    z_1,a_1,z_2,a_2 = feedforward_hidden(X, W_1, b_1, W_2, b_2)
                    data_plot[num]=[X,a_1,a_2, 'r']
                    
                elif int(num) < 666:

                    z_1,a_1,z_2,a_2 = feedforward_hidden(X, W_1, b_1, W_2, b_2)
                    data_plot[num]=[X,a_1,a_2, 'b']
       
                else:

                    z_1,a_1,z_2,a_2 = feedforward_hidden(X, W_1, b_1, W_2, b_2)
                    data_plot[num]=[X,a_1,a_2, 'g']

    x_org=[]
    y_org=[]
    z_org=[]
    x_a1=[]
    y_a1=[]
    z_a1=[]
    x_a2=[]
    y_a2=[]
    z_a2=[]
    color=[]
    
    for i in range(1000):
        i="{0:03}".format(i)

        X,a_1,a_2, color_i = data_plot[str(i)]

        # org data plot
        x_org.append(X[0])
        y_org.append(X[1])
        z_org.append(X[2])

        # first activation plot
        x_a1.append(a_1[0])
        y_a1.append(a_1[1])
        z_a1.append(a_1[2])

        # final activation plot
        x_a2.append(a_2[0])
        y_a2.append(a_2[1])
        z_a2.append(a_2[2])
        
        color.append(color_i)


    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x_org,y_org,z_org,color=color)
    plt.show()
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x_a1,y_a1,z_a1,color=color)
    plt.show()
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x_a2,y_a2,z_a2,color=color)
    plt.show()

    ### END VISUALIZATIONS ###
if __name__ == '__main__':
    with_hidden_layer_demo()
