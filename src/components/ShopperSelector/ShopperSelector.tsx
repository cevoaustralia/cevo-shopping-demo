import { FC, useEffect } from "react"

import { useStore } from "app-state/app-state"
import Loader from "components/Loader"
import { useShopperPersonas } from "hooks/useShopperPersonas"
import { useShoppers } from "hooks/useShoppers"
import { OptionType } from "models"
import * as S from './style'

export const getFilter = (persona: OptionType | OptionType[] | null) => {
  if (persona && !Array.isArray(persona) && persona.value !== "") {
    return [persona.value]
  }
}

export const isValidPersona = (persona: OptionType | OptionType[] | null) => {
  return persona &&
    !Array.isArray(persona) &&
    persona.value !== ""
}

const ShopperSelector: FC = () => {
    const { isFetching, data } = useShopperPersonas()
    const { persona, setPersona, setUserId } = useStore((state) => (
      { persona: state.persona,
        setPersona: state.setPersona,
        setUserId: state.setUserId
      }))
    const { isFetching: isShoppersFetching, data: shoppers } = useShoppers(getFilter(persona))
    
    useEffect(() => {
      if (shoppers && shoppers.length > 0 && isValidPersona(persona)) {
        setUserId(shoppers[0].id)
      }
      else {
        setUserId("")
      }
    }, [persona, setUserId, shoppers])

    const handleChange = (option: OptionType | OptionType[] | null) => {
      setPersona(option)
      console.log({ option })
      
    }

    const getLabelFromValue = (personas: string) => {
      return personas
        .split("_")
        .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
        .join(", ")
    }

    const getPersonas = (): OptionType[] | undefined =>  {
      const personas = data?.map((item): OptionType => {
        return {
          value: item,
          label: getLabelFromValue(item)
        }})

        personas?.unshift({value: "", label: "No shopper selection"})
        return personas
    }

    const getGender = (g: string) => {
      return g.toLowerCase() === "f" ? "Female" : "Male"
    }

      return (
        <S.ShopperSelector>
            {isFetching &&  <Loader />}
            <>
              <div>Pick a shopper based on Shopper Persona:</div>
              <S.Selector
                options={getPersonas()}
                value={persona}
                // eslint-disable-next-line @typescript-eslint/no-explicit-any
                onChange={(option: any) => {
                  console.log({option})
                  handleChange(option)
                }}/>
                {isValidPersona(persona)
                ?
                  <>
                    {isShoppersFetching
                    ? 
                      <Loader />
                    : 
                      <>
                        {shoppers && `Shopper: ${shoppers[0].name }
                        , ${getGender(shoppers[0].gender)}
                        , ${shoppers[0].age} years old`}
                      </>
                    }
                  </>
                  :
                  <>Shopper: No selection</>
                }
            </>
        </S.ShopperSelector>
      )
  }
  
  export default ShopperSelector
  