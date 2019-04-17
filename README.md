# Create kanji characters datasets

## Introduction

I want to create a CNN that recognizes ~2000 [Jouyou kaji](https://en.wikipedia.org/wiki/J%C5%8Dy%C5%8D_kanji) in order to make my Japanese study journey more interesting than just *cramming* [Anki](https://github.com/dae/anki) decks.

I made[ an application](https://github.com/kuroemon2509/handwriting_canvas) that allows user to draw anything and save as image so that I can use it as *training* data. However, it was a mundane task so here we are

***Creating datasets from `fonts` and some `math`.***

## Samples

- Multiple `fonts`

![HGKyokashotai](sample_images/HGKyokashotai_愛_size_96_rotate_0_x_0_y_0.png "HGKyokashotai")
![KanjiStrokeOrders](sample_images/Stroke_Orders_愛_size_96_rotate_0_x_0_y_0.png "Kanji Stroke Orders")

- Mutilple `font_size`

![HGKyokashotai_96px](sample_images/HGKyokashotai_愛_size_96_rotate_0_x_0_y_0.png "HGKyokashotai 96px")
![HGKyokashotai_144px](sample_images/HGKyokashotai_愛_size_144_rotate_0_x_0_y_0.png "HGKyokashotai 144px")

- Rotation

![HGKyokashotai_-10_degrees](sample_images/HGKyokashotai_愛_size_144_rotate_-10_x_0_y_0.png "HGKyokashotai rotate -10 degrees")
![HGKyokashotai_10_degrees](sample_images/HGKyokashotai_愛_size_144_rotate_10_x_0_y_0.png "HGKyokashotai rotate 10 degrees")

- Translation

![HGKyokashotai](sample_images/HGKyokashotai_愛_size_96_rotate_0_x_-16_0_y_32_0.png "HGKyokashotai")
![HGKyokashotai](sample_images/HGKyokashotai_愛_size_96_rotate_0_x_32_0_y_-32_0.png "HGKyokashotai")
![HGKyokashotai](sample_images/HGKyokashotai_愛_size_96_rotate_0_x_32_0_y_32_0.png "HGKyokashotai")

- Invert color

![HGKyokashotai](sample_images/HGKyokashotai_愛_size_96_rotate_0_x_0_y_0.png "HGKyokashotai")
![HGKyokashotai](sample_images/HGKyokashotai_inv_愛_size_96_rotate_0_x_0_y_0.png "HGKyokashotai inverted")