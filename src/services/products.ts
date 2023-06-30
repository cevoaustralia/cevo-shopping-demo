import axios from 'axios'

import { stringify } from "qs"
import { IGetProductsResponse } from 'models'

/** Pass category and/or user_id (to pass to Amazon Personalize) */
export const getProducts = async (filters?: string[], user_id?: string) => {
    let response: IGetProductsResponse
    const products_endpoint = `https://58spt4nge9.execute-api.ap-southeast-2.amazonaws.com/Prod/products`

    if (filters?.length || user_id) {
        const params = stringify({
                user_id,
                filters,
            },
            { skipNulls: true })

        response = await axios.get(`${products_endpoint}?${params}`)
    } else {
        response = await axios.get(products_endpoint)
    }

    const data = response.data || []
    return data
}