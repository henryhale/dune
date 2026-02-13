const isBrowser = import.meta.env.VITE_APP === 'browser'

console.log(isBrowser ? "browser" : "server")

async function predict(input: string) {
    const api = await (isBrowser ? import("./browser") : import("./server"))
    return await api.makePrediction(input)
}

export const PREDICTION_API = { predict }