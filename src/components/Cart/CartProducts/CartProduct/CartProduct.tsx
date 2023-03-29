import formatPrice from 'utils/formatPrice'
import { ICartDemoProduct } from 'models'
import { useCart } from 'contexts/cart-context'
import * as S from './style'

type IProps = {
    product: ICartDemoProduct;
}
const CartProduct = ({ product }: IProps) => {
    const { removeProduct, increaseProductQuantity, decreaseProductQuantity } =
    useCart()
    const {
      image,
      name,
      price,
      quantity
  } = product

    const handleRemoveProduct = () => removeProduct(product)
    const handleIncreaseProductQuantity = () => increaseProductQuantity(product)
    const handleDecreaseProductQuantity = () => decreaseProductQuantity(product)
    const currencyId = "AUD"
    const currencyFormat = "$"

    return (
      <S.Container>
          <S.DeleteButton
              onClick={handleRemoveProduct}
              title="remove product from cart"
            />
          <S.Image
              src={image}
              alt={name}
            />
          <S.Details>
              <S.Title>{name}</S.Title>
              <S.Desc>
                  Quantity: {quantity}
                </S.Desc>
            </S.Details>
          <S.Price>
              <p>{`${currencyFormat}  ${formatPrice(price, currencyId)}`}</p>
              <div>
                  <S.ChangeQuantity
                      onClick={handleDecreaseProductQuantity}
                      disabled={quantity === 1 ? true : false}
                    >
                      -
                    </S.ChangeQuantity>
                  <S.ChangeQuantity onClick={handleIncreaseProductQuantity}>
                      +
                    </S.ChangeQuantity>
                </div>
            </S.Price>
        </S.Container>
    )
}

export default CartProduct
