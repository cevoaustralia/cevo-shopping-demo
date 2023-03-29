import { Link } from 'react-router-dom'

import { GithubCorner } from 'components/Github'
import Loader from 'components/Loader'
import * as S from './style'
import logo from '../../../CEVO-logo-smaller.webp'
import Cart from 'components/Cart'
import { useCategories } from 'hooks/useCategories'
import Categories from '../Categories'

const CategoriesWrapper = () => {
    const { isFetching, data } = useCategories()
    const getFoundText = () => {
      if (data?.length) {
        if (data?.length === 1) { 
          return "1 Category found"
        } else {
          return `${data?.length} Categories found`
        }
      } else {
        return "No Categories found"
      }
    }

    return (
        <S.Container>
        {isFetching && <Loader />}
        <GithubCorner />
        <S.CevoLogo src={logo} alt="Cevo Logo"></S.CevoLogo>
        <S.OneColumnGrid>
            <S.Main>
                <S.Title>E-Commerce (using Amazon Personalize)</S.Title>
                <div><Link to="/">PRODUCTS</Link></div>
                <div>CATEGORIES</div>
                <S.MainHeader>
                  <p>{getFoundText()}</p>
                  </S.MainHeader>
                <Categories categories={data?.length ? data : [] } />
              </S.Main>
          </S.OneColumnGrid>
        <Cart />
      </S.Container>
    )
}

export default CategoriesWrapper
