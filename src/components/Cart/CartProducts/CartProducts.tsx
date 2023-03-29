import { ICartDemoProduct } from 'models'
import CartProduct from './CartProduct'
import * as S from './style'

type IProps = {
    products: ICartDemoProduct[];
}

const CartProducts = ({ products }: IProps) => {
    return (
      <S.Container>
          {products?.length ? (
                products.map((p, i) => <CartProduct product={p} key={i} />)
            ) : (
              <S.CartProductsEmpty>
                  Add some products in the cart <br />
                  :)
                </S.CartProductsEmpty>
            )}
        </S.Container>
    )
}

export default CartProducts
