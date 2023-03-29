import axios from 'axios'
import { stringify } from "qs"

import aws_exports from '../aws-exports'
import { ShopperResponse } from 'models'

export const getShoppers = async (filters?: string[]) => {
    let response: ShopperResponse
    const baseUrl = `${aws_exports.aws_cloud_logic_custom[0].endpoint}/users`

    if (filters?.length) {
        const params = stringify({
            persona: filters[0]
        })
        response = await axios.get(
            `${baseUrl}?${params}`
        )
    } else {
        // no filters will return all available shoppers
        response = await axios.get(`${baseUrl}`)
    }

    const data = response.data || []
    return data
}

export const getShopperPersonas = async (filters?: string[]) => {
    let response: ShopperResponse
    const baseUrl = `${aws_exports.aws_cloud_logic_custom[0].endpoint}/users/persona`

    // no filters and /persona will return all available personas
    response = await axios.get(baseUrl)

    const data = response.data || []
    return data
}