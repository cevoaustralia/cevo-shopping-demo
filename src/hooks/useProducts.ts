import { QueryKey, useQuery, UseQueryResult } from '@tanstack/react-query'

import { getProducts } from '../services/products'
import { IDemoProduct } from '../models'

export const useProducts = (filters?: string[], user_id?: string): UseQueryResult<IDemoProduct[]> => {
  const queryKey: QueryKey = [
    'products-normal',
    filters,
    user_id
  ]
  return useQuery(
    queryKey,
    async () => (await getProducts(filters, user_id)),
    {
      staleTime: 60 * (60 * 1000), // 1 hour
      onSuccess: (data: IDemoProduct[]): void => {
        console.log(`GetProducts API success: ${data.length} items`)
      },
      onError: (error: Error): void => {
        const customMsg = 'Unspecified Error'
        console.log(`GetProducts API error: ${error.message} - ${customMsg}`)
      }
    })
}
