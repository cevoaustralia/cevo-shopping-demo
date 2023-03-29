export type IProduct = {
    id: number;
    sku: number;
    title: string;
    description: string;
    availableSizes: string[];
    style: string;
    price: number;
    installments: number;
    currencyId: string;
    currencyFormat: string;
    isFreeShipping: boolean;
}
export type IDemoProduct = {
    category: string;
    current_stock: number;
    description: string;
    gender_affinity: string;
    id: string;
    image: string;
    name: string;
    price: number;
    style: string;
    where_visible: string;
    aliases?: string[];
    image_license?: string;
    link?: string;
    installments: number;
}

export type IDemoCategory = {
    id: string;
    image: string;
    name: string;
    has_gender_affinity: string;
}

export type ICartDemoProduct = {
    quantity: number;
} & IDemoProduct

export type ITrendingProduct = {
    order: number;
} & IProduct

export type IRecommendedProduct = {
    order: number;
} & IProduct

export type ICartProduct = {
    quantity: number;
} & IProduct

export type ICartTotal = {
    productQuantity: number;
    installments: number;
    totalPrice: number;
    currencyId: string;
    currencyFormat: string;
}

export type IGetProductsResponse = {
    data: {
        products: IDemoProduct[];
    };
}

export type IGetCategoriesResponse = {
    data: {
        products: IDemoCategory[];
    };
}

export type Shopper = {
    id: string;
    name: string;
    persona: string;
    age: number;
    gender: string;
}

export type ShopperResponse = {
    data: {
        shoppers: Shopper[];
    };
}

export type ShopperPersonaResponse = {
    data: {
        personas: string[];
    };
}

export type OptionType = {
    value: string;
    label: string;
}