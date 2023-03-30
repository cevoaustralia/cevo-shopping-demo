import { GithubCorner } from 'components/Github'
import Loader from 'components/Loader'

import * as S from './style'
import logo from '../../../CEVO-logo-smaller.webp'
import { useProducts } from 'hooks/useProducts'
import Products from '../Products'
import Cart from 'components/Cart'
import { FC, useState } from 'react'
import { IDemoCategory } from 'models'
import ShopperSelector from 'components/ShopperSelector/ShopperSelector'
import { useStore } from 'app-state/app-state'

type FilterChecked = {
  name: string;
  checked: boolean;
}

type Props = {
  categories: IDemoCategory[];
}

const ProductsWrapper: FC<Props> = ({ categories }) => {
  const { userId } = useStore((state) => (
    { userId: state.userId,
    }))

    const getFoundText = () => {
      if (data?.length) {
        if (userId === "") { 
          return "Trending products"
        } else {
          return "Inspired by your shopping trends"
        }
      }
      return ""
    }

    const [categoriesFilter] = useState<FilterChecked[] | undefined>(
      categories.map((category: IDemoCategory) => {return {name: category.name, checked: false}}))
    const availableCategories: string[] | undefined = categories.map((category: IDemoCategory) => category.name)
    const getCategoriesFilter = () => {
      const filters: FilterChecked[] = []
      availableCategories?.forEach((category, index) => {
        if (categoriesFilter && categoriesFilter[index].checked === true) filters.push({  name: category, checked: false })
      })
      return filters
    }

    const { isFetching, data } = useProducts(
      getCategoriesFilter().map((category) => category.name), userId === "" ? undefined : userId)

    return (
        <S.Container>
        {isFetching && <Loader />}
        <GithubCorner />
        <S.CevoLogo src={logo} alt="Cevo Logo"></S.CevoLogo>
        <S.OneColumnGrid>
          {/* <S.Side>
            <Filter categoriesFilter={categoriesFilter} setCategoriesFilter={setCategoriesFilter}/>
          </S.Side> */}
          <S.Main>
              <S.Title>E-Commerce (using Amazon Personalize)</S.Title>
              {/* <div>PRODUCTS</div>
              <div><Link to="/categories">CATEGORIES</Link></div> */}
              <S.MainHeader>
                <div>{getFoundText()}</div>
                <ShopperSelector />
              </S.MainHeader>
              <Products products={data?.length ? data : [] } />
            </S.Main>
        </S.OneColumnGrid>
        <Cart />
      </S.Container>
    )
}

export default ProductsWrapper
