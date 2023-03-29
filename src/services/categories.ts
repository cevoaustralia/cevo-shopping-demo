import axios from 'axios'

import { IGetCategoriesResponse } from 'models'
import aws_exports from '../aws-exports'

export const getCategories = async () => {
    let response: IGetCategoriesResponse

    response = await axios.get(
        `${aws_exports.aws_cloud_logic_custom[0].endpoint}/categories`
    )

    const categories = response.data || []

    return categories
}

