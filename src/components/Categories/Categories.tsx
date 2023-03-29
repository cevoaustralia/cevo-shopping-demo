import { IDemoCategory } from 'models'
import Category from './Category'

import * as S from './style'

type IProps = {
    categories: IDemoCategory[];
}

const Categories = ({ categories }: IProps) => {
    return (
      <S.Container>
          {categories?.map((p, i) => (
              <Category category={p} key={i} />
            ))}
        </S.Container>
    )
}

export default Categories
