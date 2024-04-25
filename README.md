# flappybird-ai

Challenges: Masking, pixel perfect collision (look at pygame docs)
Mask for the top pipe and bottom pipe
if these pixels are overlapping
point of

Neural Networks
Input Layer - information to our network
Top pipe and bottom pipe
Output Layer - Jump? represented in neural layer

1. Use connections and weights (how strong the connection is)
2. Use weighted sum to get output
3. Add Bias to adjust the network to the right dimensional space
   F = Activation function ; using tanh here

NEAT - Neuroevolution of Augmenting Topologies (Check more on NEAT docs)
Initial population of birds - random

1. Each bird in the population has neural network that controls it
2. Test each of these networks and evaluate their fitness (how well they do )
3. Take the best of the last population -> Mutate and breed the best of the last population to create new population
4. Repeat until the perfromance of the birds is good

Inputs - Bird y, top pipe, bottom pipe
outputs - jump?
Activation function - tanh
Population size - 100
Fitness function - every frame the bird is further the more fit it is / distance
Max generations - 30

Config file

- seperates the species together into species and goes extinct if reset_on_extinction: False
- no new random population is created

Default Genome

- initial values
