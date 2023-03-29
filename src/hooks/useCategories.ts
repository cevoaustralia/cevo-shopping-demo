import { QueryKey, useQuery, UseQueryResult } from '@tanstack/react-query'

import { IDemoCategory } from '../models'
import { getCategories } from 'services/categories'

export const useCategories = (): UseQueryResult<IDemoCategory[]> => {
  const queryKey: QueryKey = [
    'categories-normal'
  ]
  return useQuery(
    queryKey,
    async () => (await getCategories()),
    {
      staleTime: 60 * (60 * 1000), // 1 hour
      onSuccess: (data: IDemoCategory[]): void => {
        console.log(`GetCategories API success: ${data.length} items`)
      },
      onError: (error: Error): void => {
        const customMsg = 'Unspecified Error'
        console.log(`GetCategories API error: ${error.message} - ${customMsg}`)
      }
    })
}
