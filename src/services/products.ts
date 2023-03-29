import axios from 'axios'

import { stringify } from "qs"
import aws_exports from '../aws-exports'
import { IGetProductsResponse } from 'models'

/** Pass category and/or user_id (to pass to Amazon Personalize) */
export const getProducts = async (filters?: string[], user_id?: string) => {
    let response: IGetProductsResponse

    if (filters || user_id) {
        const params = stringify({
                user_id,
                filters,
            },
            { skipNulls: true })

        response = await axios.get(
            `${aws_exports.aws_cloud_logic_custom[0].endpoint}/products?${params}`
        )
    } else {
        response = await axios.get(
            `${aws_exports.aws_cloud_logic_custom[0].endpoint}/products`
        )
    }

    const data = response.data || []
    return data
}