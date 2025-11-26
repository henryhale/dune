// import * as ort from "onnxruntime-web"

// /**
//  * Load ONNX model and make a prediction on text input
//  * 
//  * @param {string|ArrayBuffer} modelPath - Path to ONNX model file or ArrayBuffer
//  * @param {string} text - Input text to classify
//  * @param {string[]} classLabels - Array of class labels (e.g., ['negative', 'positive'])
//  * @returns {Promise<{class: string, probability: number, allProbabilities: object}>}
//  */
// export async function predictText(modelPath: string, text: string, classLabels: string[] | null = null) {
//   try {
//     // Load the ONNX model
//     let session;
//     if (typeof modelPath === 'string') {
//       session = await ort.InferenceSession.create(modelPath);
//     } else {
//       session = await ort.InferenceSession.create(modelPath);
//     }
    
//     console.log('Model loaded successfully');
//     console.log('Input names:', session.inputNames);
//     console.log('Output names:', session.outputNames);
    
//     // Get input and output names
//     const inputName = session.inputNames[0]!;
//     const outputNames = session.outputNames;
    
//     // Find the probability output (usually named 'probabilities' or 'output_probability')
//     const probOutputName = outputNames.find(name => 
//       name.includes('probab') || name === 'output_probability'
//     ) || outputNames[1] || outputNames[0];
    
//     // Find the label output (usually named 'label' or 'output_label')
//     const labelOutputName = outputNames.find(name => 
//       name.includes('label') && !name.includes('probab')
//     ) || outputNames[0]!;
    
//     // Prepare input - sklearn TF-IDF pipeline expects string input
//     // Create a string tensor
//     const inputTensor = new ort.Tensor('string', [text], [1]);
    
//     // Create feeds object
//     const feeds: Record<string, any> = {};
//     feeds[inputName] = inputTensor;
    
//     // Run inference
//     const output = await session.run(feeds);
    
//     console.log('Available outputs:', Object.keys(output));
    
//     // Get the predicted label
//     let predictedClass;
//     if (output[labelOutputName]) {
//       const labelData = output[labelOutputName].data;
//       const labelIndex = typeof labelData[0] === 'bigint' ? Number(labelData[0]) : labelData[0];
      
//       if (classLabels && Array.isArray(classLabels) && classLabels.length > labelIndex) {
//         predictedClass = classLabels[labelIndex];
//       } else {
//         predictedClass = String(labelData[0]);
//       }
//     }
    
//     // Get probabilities if available
//     let probability = 0;
//     let allProbabilities = {};
    
//     if (output[probOutputName]) {
//       const probTensor = output[probOutputName];
      
//       // Handle different probability output formats
//       if (probTensor.dims.length === 3) {
//         // Format: [1, 1, num_classes] - common for sklearn models
//         const probabilities = Array.from(probTensor.data);
//         const maxProb = Math.max(...probabilities);
//         const maxProbIndex = probabilities.indexOf(maxProb);
        
//         probability = maxProb;
        
//         // Build all probabilities object
//         probabilities.forEach((prob, idx) => {
//           const label = (classLabels && classLabels[idx]) ? classLabels[idx] : `Class ${idx}`;
//           allProbabilities[label] = prob;
//         });
        
//         // If class wasn't determined yet, use argmax
//         if (!predictedClass) {
//           predictedClass = (classLabels && classLabels[maxProbIndex]) ? 
//             classLabels[maxProbIndex] : `Class ${maxProbIndex}`;
//         }
//       } else if (probTensor.dims.length === 2) {
//         // Format: [1, num_classes]
//         const probabilities = Array.from(probTensor.data);
//         const maxProb = Math.max(...probabilities);
//         const maxProbIndex = probabilities.indexOf(maxProb);
        
//         probability = maxProb;
        
//         probabilities.forEach((prob, idx) => {
//           const label = (classLabels && classLabels[idx]) ? classLabels[idx] : `Class ${idx}`;
//           allProbabilities[label] = prob;
//         });
        
//         if (!predictedClass) {
//           predictedClass = (classLabels && classLabels[maxProbIndex]) ? 
//             classLabels[maxProbIndex] : `Class ${maxProbIndex}`;
//         }
//       } else {
//         // Single value probability
//         probability = Array.from(probTensor.data)[0];
//         allProbabilities[predictedClass] = probability;
//       }
//     } else {
//       // If no probability output, set to 1.0 for the predicted class
//       probability = 1.0;
//       if (predictedClass) {
//         allProbabilities[predictedClass] = 1.0;
//       }
//     }
    
//     return {
//       class: predictedClass,
//       probability: probability,
//       allProbabilities: allProbabilities
//     };
    
//   } catch (error) {
//     console.error('Prediction error:', error);
//     throw error;
//   }
// }

