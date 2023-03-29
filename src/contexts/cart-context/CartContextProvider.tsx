import { createContext, useContext, useState } from 'react'

import { ICartDemoProduct, ICartTotal } from 'models'

export type ICartContext = {
    isOpen: boolean;
    setIsOpen(state: boolean): void;
    products: ICartDemoProduct[];
    setProducts(products: ICartDemoProduct[]): void;
    total: ICartTotal;
    setTotal(products: ICartTotal): void;
}

const CartContext = createContext<ICartContext | undefined>(undefined)
const useCartContext = (): ICartContext => {
    const context = useContext(CartContext)

    if (!context) {
        throw new Error('useCartContext must be used within a CartProvider')
    }

    return context
}

const totalInitialValues = {
    productQuantity: 0,
    installments: 0,
    totalPrice: 0,
    currencyId: 'USD',
    currencyFormat: '$',
}

type Props = {
    children?: React.ReactNode;
}

const CartProvider = (props: Props) => {
    const [isOpen, setIsOpen] = useState(false)
    const [products, setProducts] = useState<ICartDemoProduct[]>([])
    const [total, setTotal] = useState<ICartTotal>(totalInitialValues)

    const CartContextValue: ICartContext = {
        isOpen,
        setIsOpen,
        products,
        setProducts,
        total,
        setTotal,
    }

    return <CartContext.Provider value={CartContextValue} {...props} />
}

export { CartProvider, useCartContext }
