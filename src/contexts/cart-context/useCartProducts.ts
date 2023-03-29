import { useCartContext } from './CartContextProvider'
import useCartTotal from './useCartTotal'
import { ICartDemoProduct } from 'models'

const useCartProducts = () => {
    const { products, setProducts } = useCartContext()
    const { updateCartTotal } = useCartTotal()

    const updateQuantitySafely = (
        currentProduct: ICartDemoProduct,
        targetProduct: ICartDemoProduct,
        quantity: number
    ): ICartDemoProduct => {
        if (currentProduct.id === targetProduct.id) {
            return Object.assign({
                ...currentProduct,
                quantity: currentProduct.quantity + quantity,
            })
        } else {
            return currentProduct
        }
    }

    const addProduct = (newProduct: ICartDemoProduct) => {
        let updatedProducts
        const isProductAlreadyInCart = products.some(
            (product: ICartDemoProduct) => newProduct.id === product.id
        )

        if (isProductAlreadyInCart) {
            updatedProducts = products.map((product: ICartDemoProduct) => {
                return updateQuantitySafely(product, newProduct, newProduct.quantity)
            })
        } else {
            updatedProducts = [...products, newProduct]
        }

        setProducts(updatedProducts)
        updateCartTotal(updatedProducts)
    }

    const removeProduct = (productToRemove: ICartDemoProduct) => {
        const updatedProducts = products.filter(
            (product: ICartDemoProduct) => product.id !== productToRemove.id
        )

        setProducts(updatedProducts)
        updateCartTotal(updatedProducts)
    }

    const increaseProductQuantity = (productToIncrease: ICartDemoProduct) => {
        const updatedProducts = products.map((product: ICartDemoProduct) => {
            return updateQuantitySafely(product, productToIncrease, +1)
        })

        setProducts(updatedProducts)
        updateCartTotal(updatedProducts)
    }

    const decreaseProductQuantity = (productToDecrease: ICartDemoProduct) => {
        const updatedProducts = products.map((product: ICartDemoProduct) => {
            return updateQuantitySafely(product, productToDecrease, -1)
        })

        setProducts(updatedProducts)
        updateCartTotal(updatedProducts)
    }

    return {
        products,
        addProduct,
        removeProduct,
        increaseProductQuantity,
        decreaseProductQuantity,
    }
}

export default useCartProducts
