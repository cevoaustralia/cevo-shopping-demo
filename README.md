## POC for a Recommendation Engine using Amazon Personalize

[Amazon Personalize](https://aws.amazon.com/personalize/) is a fully managed machine learning service (Recommendation Engine) that uses your data to generate item recommendations for your users. It can also generate user segments based on the users' affinity for certain items or item metadata.

Building **Recommendation Systems** is hard to do well, let Amazon do the heavy lifting for you.

This system covers a few common use cases, and although fully managed, you will still need to supply your own data, either through **streaming** ingestion or **batching**. As a high level AI service, you don't need to know any Machine Learning concepts like **model selection**, **hyperparameter optimisation**, **experiment tracking**, or even **inference hosting**, since that is all handled for you.

After supplying the data and training the model, the recommendations are then available through **API calls**.

For this POC, we will have:

- [fictitious E-Commerce website repo](https://github.com/jaeyow/react-shopping-cart)
- with user personas, items and interactions [simulated like what was done here](https://github.com/aws-samples/retail-demo-store).

Here are a list of things we want to find out:

1. Why do we need personalization
2. How to plug in our own data to it
3. What recommender recipe to use with what type of problem
4. How to tune recommendations
5. How to create campaigns from the AWS Console
6. How to create campaigns from script
7. How to do realtime, then batch prediction
8. How to mix business rules with the predictions
9. How to handle User cold starts
10. How to handle Item cold starts
11. How to integrate with Amazon Pinpoint

```javascript
/* First, Install the needed packages */
yarn install

/* Then start the React app */
yarn start

```

### Copyright and license

The MIT License (MIT). Please see License File for more information.

<br/>
<br/>

<sub>Adapted with thanks from <a href="http://www.jeffersonribeiro.com/">Jefferson Ribeiro</a></sub>

</p>
