namespace Domain.Models.Queries
{
    public class BookingQuery : BaseQuery
    {
        public string SearchString { get; set; }
        public string CheckinDate { get; set; }
        public string CheckoutDate { get; set; }
        public int MinBudget { get; set; }
        public int MaxBudget { get; set; }
        public int NumberOfAdults { get; set; }
        public int NumberOfChildren { get; set; }
        public int NumberOfRooms { get; set; }
        public string Language { get; set; }
        public string Currency { get; set; }
        public string UserCountry { get; set; }

        public BookingQuery(FilteringModel filteringModel)
        {
            var durationInDays = (filteringModel.CheckOut - filteringModel.CheckIn).Days;
            SearchString = $"{filteringModel.Destination.City}, {filteringModel.Destination.Country}";
            CheckinDate = filteringModel.CheckIn.ToString("YYYY-MM-DD");
            CheckoutDate = filteringModel.CheckOut.ToString("YYYY-MM-DD");
            MaxBudget = (int)filteringModel.Budget.Max / durationInDays;
            MinBudget = (int)filteringModel.Budget.Min / durationInDays;
            NumberOfAdults = filteringModel.Travelers.Adults;
            NumberOfChildren = filteringModel.Travelers.Children;
            NumberOfRooms = filteringModel.Accommodation.Rooms;
            Language = filteringModel.UserLanguage;
            Currency = filteringModel.UserCurrency;
            UserCountry = filteringModel.UserCountry;
        }
    }
}