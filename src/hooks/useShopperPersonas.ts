import { QueryKey, useQuery, UseQueryResult } from '@tanstack/react-query'

import { getShopperPersonas } from 'services/shopper'

export const useShopperPersonas = (filters?: string[]): UseQueryResult<string[]> => {

  const queryKey: QueryKey = [
    'shopper-personas',
    filters
  ]
  return useQuery(
    queryKey,
    async () => (await getShopperPersonas()),
    {
      staleTime: 60 * (60 * 1000), // 1 hour
      onSuccess: (data: string[]): void => {
        console.log(`GetShopperPersonas API success: ${data.length} items`)
      },
      onError: (error: Error): void => {
        const customMsg = 'Unspecified Error'
        console.log(`GetShopperPersonas API error: ${error.message} - ${customMsg}`)
      }
    })
}
