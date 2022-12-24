import { View, Text, ScrollView } from 'react-native'
import React, { useEffect } from 'react'
import { ArrowRightIcon } from 'react-native-heroicons/outline'
import RestaurantCard from './RestaurantCard'

const FeaturedRow = ({ id, title, description }) => {
  const [restaurants, setRestaurants ] = useState([]);

  useEffect(() => {
    sanityClient.fetch(
      `
      *l_type == "featured" && _id == $id {
        ...,
        restaurants[]->{
          ...,
          dishes[]->,
          type-> {
            name
          }
        },
      }[0]
      `, {id}
    ).then((data) => {
      setRestaurants(data?.restaurants)
    })
  }, [])

  return (
    <View>
      <View className="mt-4 flex-row items-center justify-between px-4">
        <Text className="font-bold text-lg">{{title}}</Text>
        <ArrowRightIcon color="#00CCBB" />
      </View>

      <ScrollView
        horizontal
        contentContainerStyle={{
          paddingHorizontal: 15
        }}
        showsHorizontalScrollIndicator={false}
        className="p-4"
      >

      {restaurants?.map((restaurant) => {
        <RestaurantCard
          key={restaurant._id}
          id={restaurant._id}
          imgUrl={restaurant.image}
          address={restaurant.address}
          title={restaurant.name}
          rating={restaurant.rating}
          genre={restaurant.type?.name}
          short_description={restaurant.short_description}
          dishes={restaurant.dishes}
          long={restaurant.long}
          lat={restaurant.lat}
       />
      })}

      </ScrollView>
    </View>
  )
}

export default FeaturedRow