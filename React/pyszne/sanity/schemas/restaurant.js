import {defineField, defineType} from 'sanity'

export default defineType({
  name: 'restaurant',
  title: 'restaurant',
  type: 'document',
  fields: [
    {
      name: "name",
      type: "string",
      title: "Restaurant name",
      validation: (Rule) => Rule.required()
    },
    {
      name: "short_description",
      type: "strinf",
      title: "Short description"
    },
    {
      name: "image",
      type: "image",
      title: "Image of the Restaurant"
    },
    {
      name: "lat",
      type: "number",
      title: "Latitude of the Restaurant"
    },
    {
      name: "long",
      type: "number",
      title: "Longitude of the restaurant",
    },
    {
      name: "address",
      type: "string",
      title: "Restaurant address",
      validation: (Rule) => Rule.required()
    },
    {
      name: "rating",
      type: "number",
      title: "Enter a Rating from (1-5 Start)",
      validation: (Rule) => Rule.required().min(1).max(5).error("Please enter a value between 1 and 5")
    },
    {
      name: "type",
      type: "string",
      title: "Category",
      validation: (Rule) => Rule.required(),
      type: "reference",
      to: [{ type: "category"}]
    },
    {
      name: "dishes",
      type: "array",
      title: "Dishes",
      efs: [{types: "reference", to: [{type: "dish"}]}]
    },
  ],
})
