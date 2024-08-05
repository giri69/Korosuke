import React from 'react'
import Header from '../components/Header'
import Hero from '../components/Hero'
import Benefits from '../components/Benefits'
import Footer from '../components/Footer'
import ButtonGradient from "../assets/svg/ButtonGradient";
const Homepage = () => {
  return (
    <>
    <div className="pt-[4.75rem] lg:pt-[5.25rem] overflow-hidden lg:bg-n-8/90">
        <Header />
        <Hero />
        <Benefits />
        <Footer />
      </div>
      <ButtonGradient />
    </>
  )
}

export default Homepage