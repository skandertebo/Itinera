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
    }
}