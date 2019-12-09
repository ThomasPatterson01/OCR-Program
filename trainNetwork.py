#https://www.coursera.org/learn/machine-learning/home/week/4
#https://docs.scipy.org/doc/numpy/reference/generated/numpy.matrix.html

#482 features (including bias unit)
#so 482 nodes in input layers
#62 nodes in output layer
#(482 + 62)/2 = 272 nodes in hidden layer

import numpy as np
from ImageManager import ImageManager

LEARNING_RATE = 3
LAMBDA = 100
ITERATIONS = 3000
SAVE_FREQUENCY = 250
EMAIL_SAVE_DATA = False
EMAIL_ADDRESS = ''
EMAIL_PASSWORD = ''
EMAIL_UPDATES = FALSE

def sigmoid(z):
    denominator = 1 + np.exp(-z)
    result = 1 / denominator
    return result
	
def loadXandYMatrices(start, end):
    xSource = []
    ySource = []
        
    with open("res/features.txt") as f:
        data = f.read()
        lines = data.split("\n")
        
        lines = lines[start:end]
        for l in lines:
            lineArr = [1]
            l = l.split(",")
            ySource.append(float(l[0]))
            
            for i in range(1, len(l)):
                lineArr.append(float(l[i]))

            xSource.append(lineArr)

    X = np.matrix(xSource)
    Y = np.matrix(ySource)

    return X, Y.getT()

def trainNetwork(theta1, theta2, k, X, y):
    m = len(X)
    sum_ = 0
    grad1 = 0
    grad2 = 0

    for i in range(m):

        #feed forward
        a1 = X[i, :].getT()
        z2 = theta1*a1
        a2 = sigmoid(z2)
        a2 = np.concatenate((np.matrix("1"), a2))
        z3 = theta2*a2
        a3 = sigmoid(z3)

        cost = 0
        Y = np.zeros((k, 1))
        Y[int(y[i])] = 1

        #cost function
        for j in range(k):
            cost += -Y[j] * np.log(a3[j]) - (1-Y[j])*np.log(1-a3[j])
        sum_ += cost

        #back prop
        delta3 = a3 - Y
        delta2 = np.multiply((theta2.getT()*delta3), np.multiply(a2, 1-a2))
        delta2 = delta2[1:]

        grad1 += delta2*a1.getT()
        grad2 += delta3*a2.getT()

    J = sum_ / m
    theta1Grad = grad1/m
    theta2Grad = grad2/m

    return J, theta1Grad, theta2Grad

def gradientDescent(X, Y, theta1, theta2, iterations):
    m = len(X)

    for i in range(iterations):
        J, theta1Grad, theta2Grad = trainNetwork(theta1, theta2, 62, X, Y)        
        
        delta1 = LEARNING_RATE * theta1Grad
        delta2 = LEARNING_RATE * theta2Grad
        
        theta1 = np.subtract(theta1, delta1)
        theta2 = np.subtract(theta2, delta2)

        print(str(i) + ": " + str(J))

        if (i % SAVE_FREQUENCY == 0):
            saveData(theta1, theta2, i)
            if (EMAIL_SAVE_DATA):
                emailUpdate(i,str(J))
    return theta1, theta2

def saveData(theta1, theta2, iterations): 
    if (iterations == 0):
        return
    
    np.savetxt("weights/" + str(LEARNING_RATE) + "-" + str(iterations) + "-theta1.txt", theta1)
    np.savetxt("weights/" + str(LEARNING_RATE) + "-" + str(iterations) + "-theta2.txt", theta2)
    
def emailUpdate(iterations, score):
    import smtplib

    if not EMAIL_UPDATES:
	return

    TO = EMAIL_ADDRESS
    SUBJECT = 'Network Update'
    TEXT = 'Iterations: ' + str(iterations) + '\nScore: ' + str(score)

    # Gmail Sign In
    gmail_sender = EMAIL_ADDRESS
    gmail_passwd = EMAIL_PASSWORD

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(gmail_sender, gmail_passwd)

    BODY = '\r\n'.join(['To: %s' % TO,
                        'From: %s' % gmail_sender,
                        'Subject: %s' % SUBJECT,
                        '', TEXT])

    try:
        server.sendmail(gmail_sender, [TO], BODY)
        print ('email sent')
    except:
        print ('error sending mail')

    server.quit()
    
def main():
    X, Y = loadXandYMatrices(0, 1116)

    np.random.seed(1)
    theta1 = (np.matrix(np.random.rand(272, 482))*2)-1
    
    theta2 = (np.matrix(np.random.rand(62 , 273))*2)-1

    theta1, theta2 = gradientDescent(X, Y, theta1, theta2, ITERATIONS)

    saveData(theta1, theta2, ITERATIONS)
    
    h1 = sigmoid(X * theta1.getT())
    a = np.ones((1116, 1))
    h1 = np.concatenate((a, h1), axis=1)
    h2 = sigmoid(h1 * theta2.getT())
       
    predictions = np.argmax(h2, axis = 1)

    correct = 0
    for i in range(len(Y)):
        if int(Y.item(i)) == int(predictions.item(i)):
            correct += 1
        print("Actual: " + str(Y[i]) + "   Predicted: " + str(predictions[i]))

    print(correct/1116)
    
if __name__ == "__main__":
    main()
    for i in range(20):
        input()


