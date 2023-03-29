import { Route, Routes }  from 'react-router-dom'

import ProductsWrapper from 'components/Products/ProductsWrapper'
import CategoriesWrapper from 'components/Categories/CategoriesWrapper'
import { useCategories } from 'hooks/useCategories'
import Loader from 'components/Loader'

function App() {
  const { isFetching, data } = useCategories()
    return (
      <>
      { isFetching && <Loader /> }
      { !isFetching &&
        <Routes>
          <Route path="/" element={<ProductsWrapper categories={data || []} />} />
          <Route path="/categories" element={<CategoriesWrapper />} />
        </Routes>}
      </>
    )
}

export default App
