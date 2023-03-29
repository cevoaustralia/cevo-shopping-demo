import { IDemoProduct } from 'models'
import Product from './Product'

import * as S from './style'

type IProps = {
    products: IDemoProduct[];
}

const Products = ({ products }: IProps) => {
    return (
      <S.Container>
          {products?.map((p, i) => (
              <Product product={p} key={i} />
            ))}
        </S.Container>
    )
}

export default Products
