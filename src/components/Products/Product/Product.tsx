import { KeyboardEvent } from 'react'

import formatPrice from 'utils/formatPrice'
import { IDemoProduct } from 'models'
import { useCart } from 'contexts/cart-context'
import * as S from './style'

type IProps = {
    product: IDemoProduct;
}

const Product = ({ product }: IProps) => {
    const { openCart, addProduct } = useCart()
    const {
        category,
        description,
        image,
        name,
        price,
        installments
    } = product
    const currencyId = "AUD"
    const currencyFormat = "$"

    const formattedPrice = formatPrice(price, currencyId)
    let productInstallment

    if (installments) {
        const installmentPrice = price / installments

        productInstallment = (
          <S.Installment>
              <span>or {installments} x</span>
              <b>
                  {currencyFormat}
                  {formatPrice(installmentPrice, currencyId)}
                </b>
            </S.Installment>
        )
    }

    const handleAddProduct = () => {
        addProduct({ ...product, quantity: 1 })
        openCart()
    }

    const handleAddProductWhenEnter = (event: KeyboardEvent) => {
        if (event.key === 'Enter' || event.code === 'Space') {
            addProduct({ ...product, quantity: 1 })
            openCart()
        }
    }

    return (
      <S.Container onKeyUp={handleAddProductWhenEnter} image={image} tabIndex={1}>
          <S.Image image={image} />
          <S.Title>{name}</S.Title>
          <S.Subtitle>{category.toUpperCase().replace("-", " ")}</S.Subtitle>
          <S.Subtitle>{description}</S.Subtitle>
          <S.Price>
              <S.Val>
                  <small>{currencyFormat}</small>
                  <b>{formattedPrice.substring(0, formattedPrice.length - 3)}</b>
                  <span>{formattedPrice.substring(formattedPrice.length - 3)}</span>
                </S.Val>
              {productInstallment}
            </S.Price>
          <S.BuyButton onClick={handleAddProduct} tabIndex={-1}>
              Add to cart
            </S.BuyButton>
        </S.Container>
    )
}

export default Product
