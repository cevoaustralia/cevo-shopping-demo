import { FC, Fragment } from 'react'

import * as S from './style'

export type FilterChecked = {
  name: string;
  checked: boolean;
}

type Props = {
  categoriesFilter: FilterChecked[] | undefined;
  setCategoriesFilter: React.Dispatch<React.SetStateAction<FilterChecked[] | undefined>>;
}

const Filter: FC<Props> = ({categoriesFilter, setCategoriesFilter}) => {
    const handleOnChange = (position: number) => {
        const updatedCheckedState: FilterChecked[] | undefined = categoriesFilter?.map((item, index) => {
          return {
            name: item.name,
            checked: position === index ? !item.checked : false
          }
        }
        )
    
        setCategoriesFilter(updatedCheckedState)
    
      }

    return (
      <S.Container>
          <S.Title>Categories:</S.Title>
          {categoriesFilter?.map((item, index) => {
                return (
                  <Fragment key={item.name}>
                    <S.CheckLabel>{item.name}</S.CheckLabel>
                    <S.Checkbox isChecked={item.checked} label="" handleOnChange={() => {handleOnChange(index)}} key={item.name} />
                  </Fragment>
                    
                )
                
            })
          }
        </S.Container>
    )
}

export default Filter
