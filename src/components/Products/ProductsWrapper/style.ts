import styled from 'styled-components/macro'

export const Container = styled.div``

export const OneColumnGrid = styled.main`
  display: grid;
  grid-template-columns: 1fr;
  max-width: 1200px;
  margin: 50px auto auto;
`

export const TwoColumnGrid = styled.main`
  display: grid;
  grid-template-columns: 1fr;
  max-width: 1200px;
  margin: 50px auto auto;
  @media only screen and (min-width: ${({ theme: { breakpoints } }) =>
        breakpoints.tablet}) {
    grid-template-columns: 1fr 4fr;
    margin-top: 80px;
  }
`

export const Side = styled.div`
  display: grid;
  justify-content: center;
  padding: 15px;
  box-sizing: border-box;

  @media only screen and (min-width: ${({ theme: { breakpoints } }) =>
        breakpoints.tablet}) {
    align-content: baseline;
  }
`
export const Main = styled.main``

export const MainHeader = styled.main`
  display: grid;
  grid-template-columns: 1fr 1fr;
  justify-content: end;
  padding: 25px 0;
`

export const Title = styled.div`
  display: flex;
  justify-content: center;
  padding: 15px;
  font-size: 1.5rem;
  font-style: bold;
`

export const CevoLogo = styled.img`
  display: flex;
  justify-content: center;
  margin: 50px auto;
`

export const ShopperSelector = styled.div`
  display: flex;
  justify-content: flex-end;
`
