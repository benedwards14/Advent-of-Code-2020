import qualified System.IO as IO
import qualified Data.List as List


find2020Product :: Integer -> [Integer] -> Integer
find2020Product combinations =
    product . head . filter (\numbs -> sum numbs == 2020) . getCombinations combinations


getCombinations :: Integer -> [Integer] -> [[Integer]]
getCombinations 0 numbers = [[]]
getCombinations n numbers =
    [ x:y | x <- numbers, y <- curr_combinations, not $ x `elem` y ]
    where
        curr_combinations = getCombinations (n-1) numbers


part1 :: [Integer] -> Integer
part1 = find2020Product 2


part2 :: [Integer] -> Integer
part2 = find2020Product 3


main :: IO ()
main = do
    contents <- IO.readFile "../data/day_1.txt"
    let numbers = map (\num -> read num :: Integer) $ lines contents
    putStrLn $ show $ part1 numbers
    putStrLn $ show $ part2 numbers