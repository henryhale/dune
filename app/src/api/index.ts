import * as browserPrediction from "./browser"
import * as serverPrediction from "./server"

export const PREDICTION_API = import.meta.env.APP === "browser" ? browserPrediction : serverPrediction
