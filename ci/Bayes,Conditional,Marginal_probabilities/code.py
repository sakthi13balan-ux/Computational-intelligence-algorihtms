#Bag contains 6 red balls and 4 blue balls.
print("\nPrior Probability")
red_balls = 6
print("Red balls: ",red_balls)
blue_balls = 4
print("Blue balls: ",blue_balls)
total_balls = red_balls + blue_balls
prob_red = red_balls / total_balls
print("Prior Probability of Red Ball =", prob_red)

print("\nBayes Theorem") 
P_A = 0.60
print("P(A): ",P_A)
P_B = 0.40
print("P(B): ",P_B)
P_D_given_A = 0.03
P_D_given_B = 0.05
print("P(D/A): ",P_D_given_A)
print("P(D/B): ",P_D_given_B)
# Total defective probability
P_D = (P_D_given_A * P_A) + (P_D_given_B * P_B)
# Bayes Formula
P_B_given_D = (P_D_given_B * P_B) / P_D
print("Probability defective item came from Machine B =", P_B_given_D)

print("\nBayesian Network")
P_Cloudy = 0.5
P_Rain_given_Cloudy = 0.8
P_Traffic_given_Rain = 0.7
print("P(cloudy): ",P_Cloudy)
print("P(Rain/Cloudy): ",P_Rain_given_Cloudy)
print("P(Traffic/rain): ",P_Traffic_given_Rain)
# Total probability
P_Traffic = P_Cloudy * P_Rain_given_Cloudy * P_Traffic_given_Rain
print("Probability of Traffic when Cloudy =", P_Traffic)

print("\nFull Joint Probability")
P_TT = 0.10
P_TF = 0.40
P_FT = 0.20
P_FF = 0.30
# P(Rain)
P_Rain = P_TT + P_TF
# P(Sprinkler)
P_Sprinkler = P_TT + P_FT
P_and = P_TT
print("P(Rain) =", P_Rain)
print("P(Sprinkler) =", P_Sprinkler)
print("P(Rain and Sprinkler)=",P_and)