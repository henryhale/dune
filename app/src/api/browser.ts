import type { APIResult } from "@/types";
import * as ort from "onnxruntime-web";
import pipelinePath from "../../public/model/pipeline.onnx?url";
import pipelineClasses from "../../public/model/classes.json";

/**
 * Load ONNX model and make a prediction on text input
 *
 * @param {string|ArrayBuffer} modelPath - Path to ONNX model file or ArrayBuffer
 * @param {string} text - Input text to classify
 * @param {string[]} classLabels - Array of class labels (e.g., ['negative', 'positive'])
 */
async function predict(
  modelPath: string,
  text: string,
  classLabels: string[] = [],
): Promise<APIResult> {
  try {
    // Load the ONNX model
    const session = await ort.InferenceSession.create(modelPath);

    console.log("Model loaded successfully");
    console.log("Input names:", session.inputNames);
    console.log("Output names:", session.outputNames);

    // Get input and output names
    const inputName = session.inputNames[0]!;
    const outputNames = session.outputNames;

    // Find the probability output (usually named 'probabilities' or 'output_probability')
    const probOutputName =
      outputNames.find((name) => name.includes("probab")) ||
      outputNames[1] ||
      outputNames[0]!;

    // Find the label output (usually named 'label' or 'output_label')
    const labelOutputName =
      outputNames.find(
        (name) => name.includes("label") && !name.includes("probab"),
      ) || outputNames[0]!;

    // Prepare input - sklearn TF-IDF pipeline expects string input
    // Create a string tensor
    const inputTensor = new ort.Tensor("string", [text], [1, 1]);

    // Create feeds object
    const feeds: Record<string, any> = {};
    feeds[inputName] = inputTensor;

    console.log("feeds", feeds);

    // Run inference
    const output = await session.run(feeds);

    console.log("Available outputs:", Object.keys(output));
    console.log("output", output);

    // Get the predicted label
    let predictedClass = "NOOP";
    if (labelOutputName in output && output[labelOutputName]) {
      const labelData = output[labelOutputName].data;
      predictedClass = String(labelData[0]);
    }
    console.log("predicted class", predictedClass);

    // Get probabilities if available
    let probability = 0;

    if (probOutputName in output && output[probOutputName]) {
      const probTensor = output[probOutputName];
      probTensor.data;
      const probabilities = [...probTensor.data].map(Number);
      const maxProb = Math.max(...probabilities);
      const maxProbIndex = probabilities.indexOf(maxProb);

      probability = maxProb;

      if (!predictedClass && maxProbIndex in classLabels) {
        predictedClass = classLabels[maxProbIndex]!;
      }
    } else {
      // If no probability output, set to 1.0 for the predicted class
      probability = 1.0;
    }

    return {
      command: predictedClass,
      confidence: probability,
      raw_text: text
    };
  } catch (error) {
    throw error;
  }
}

export async function makePrediction(input: string): Promise<APIResponse> {
    try {
        const result = await predict(pipelinePath, input, pipelineClasses)
        return {status: "success", message: "model responded", action: result}
    } catch (error) {
        return {status: "error", message: "something went wrong", action: null}
    }
}
