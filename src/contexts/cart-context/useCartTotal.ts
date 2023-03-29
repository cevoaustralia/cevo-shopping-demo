import { useCartContext } from './CartContextProvider'
import { ICartDemoProduct } from 'models'

const useCartTotal = () => {
    const { total, setTotal } = useCartContext()

    const updateCartTotal = (products: ICartDemoProduct[]) => {
        const productQuantity = products.reduce(
            (sum: number, product: ICartDemoProduct) => {
                sum += product.quantity
                return sum
            },
            0
        )

        const totalPrice = products.reduce((sum: number, product: ICartDemoProduct) => {
            sum += product.price * product.quantity
            return sum
        }, 0)

        const installments = products.reduce(
            (greater: number, product: ICartDemoProduct) => {
                greater =
          product.installments > greater ? product.installments : greater
                return greater
            },
            0
        )

        const total = {
            productQuantity,
            installments,
            totalPrice,
            currencyId: 'USD',
            currencyFormat: '$',
        }

        setTotal(total)
    }

    return {
        total,
        updateCartTotal,
    }
}

export default useCartTotal
