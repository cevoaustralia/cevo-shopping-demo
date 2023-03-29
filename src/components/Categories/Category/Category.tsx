
import { IDemoCategory } from 'models'
import * as S from './style'

type IProps = {
    category: IDemoCategory;
}

const Category = ({ category }: IProps) => {
    const {
        name,
        image
    } = category

    return (
      <S.Container image={image} tabIndex={1}>
        <S.Image image={image} />
        <S.Title>{name.toUpperCase().replace("-", " ")}</S.Title>
    </S.Container>
    )
}

export default Category
