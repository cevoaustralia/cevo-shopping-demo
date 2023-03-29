import { QueryKey, useQuery, UseQueryResult } from '@tanstack/react-query'

import { useStore } from 'app-state/app-state'
import { isValidPersona } from 'components/ShopperSelector/ShopperSelector'
import { Shopper } from 'models'

import { getShoppers } from 'services/shopper'

export const useShoppers = (filters?: string[]): UseQueryResult<Shopper[]> => {
  const { setUserId, persona } = useStore((state) => (
      {
        persona: state.persona,
        setUserId: state.setUserId
      }
    ))

  const queryKey: QueryKey = [
    'shoppers',
    filters
  ]
  return useQuery(
    queryKey,
    async () => (await getShoppers(filters)),
    {
      staleTime: 60 * (60 * 1000), // 1 hour
      onSuccess: (data: Shopper[]): void => {
        console.log(`GetShoppers API success: ${data.length} items`)
        if (isValidPersona(persona)) {
          // save shopper in global state
          setUserId(data[0].id)
        }
      },
      onError: (error: Error): void => {
        const customMsg = 'Unspecified Error'
        console.log(`GetShoppers API error: ${error.message} - ${customMsg}`)
      }
    })
}
